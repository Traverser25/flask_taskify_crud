from flask import Blueprint, request, jsonify
from app.models import Task, User
from app.extensions import db
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt 
from app.utils.jwt_helper import auth_required
from app.schemas.task_schema import TaskCreate
from app.schemas.task_update_schema import  TaskUpdate
from pydantic import ValidationError
from app.utils.api_response import success_response,error_response
task_bp = Blueprint('task_bp', __name__)

from sqlalchemy import or_
from datetime import datetime

from app.utils.api_response import success_response, error_response
from app.utils.logger import logger


#===============================================Helper Functions==============================
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def fetch_tasks(user_id, filter_by='assigned_to'):
    # Query parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    priority = request.args.get('priority')
    search = request.args.get('search')
    due_before = parse_date(request.args.get('due_before'))
    due_after = parse_date(request.args.get('due_after'))

    # Choose the filter dynamically
    base_filter = {
        'assigned_to': Task.assigned_to == user_id,
        'assigned_by': Task.assigned_by == user_id
    }.get(filter_by)

    if base_filter is None:
        raise ValueError("Invalid filter_by value")

    query = Task.query.filter(base_filter)

    # Apply filters
    if status:
        query = query.filter(Task.status == int(status))
    if priority:
        query = query.filter(Task.priority == int(priority))
    if search:
        query = query.filter(or_(
            Task.title.ilike(f"%{search}%"),
            Task.description.ilike(f"%{search}%")
        ))
    if due_before:
        query = query.filter(Task.due_date <= due_before)
    if due_after:
        query = query.filter(Task.due_date >= due_after)

    # Pagination
    total_items = query.count()
    offset = (page - 1) * page_size
    tasks = query.order_by(Task.id.desc()).offset(offset).limit(page_size).all()

    task_list = [{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "due_date": str(t.due_date) if t.due_date else None,
        "priority": t.priority,
        "status": t.status,
        "assigned_to": t.assigned_to,
        "assigned_by": t.assigned_by
    } for t in tasks]

    total_pages = (total_items + page_size - 1) // page_size
    return {
        "tasks": task_list,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_previous": page > 1,
            "has_next": page < total_pages
        }
    }


#========================================================================================================================







#=======================================================ADD TASK ROUTE========================================#


@task_bp.route('/add_task', methods=['POST'])
@jwt_required() # Protect this route by requiring a valid JWT token
def create_task():
    try:
        task_data = TaskCreate(**request.json)
                                                 
        cur_user = get_jwt_identity()
        if task_data.assigned_to == cur_user:
            return jsonify(error_response("Cannot assign task to yourself")), 400

        task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            status=task_data.status,
            assigned_by=cur_user,
            assigned_to=task_data.assigned_to
        )

        db.session.add(task)
        db.session.commit()
        logger.info(f"Task  added by the user  {cur_user}")
        res = success_response("Task created successfully", {"task_id": task.id}, 201)
        return jsonify(res["response"]), res["status_code"]

    except ValidationError as e:
        logger.error(f"Error in ad task from user id {cur_user}")
        error_msgs = [err['msg'] for err in e.errors()]
        res = error_response("Validation failed", error_msgs, 400)
        return jsonify(res["response"]), res["status_code"]
    
#=======================================================================================================================#





#=======================================================UPDATE TASK ROUTE===============================================#

@task_bp.route('/update_task/<int:task_id>', methods=['POST'])
@jwt_required()  # Protect this route by requiring a valid JWT token
def update_task(task_id):
    try:
        # Get the current user's ID from JWT
        cur_user = get_jwt_identity()

        # Fetch the task from the database, return a 404 if not found
        task = Task.query.get(task_id)
        
        # If the task is not found, return an error message
        if not task:
            return jsonify(error_response("Task not found")), 404

        # Parse and validate the incoming JSON body with Pydantic
        task_data = TaskUpdate(**request.json)  # Use the TaskUpdate model to validate input data

        # If the task is being updated, we ensure we are not assigning it to the current user
        if task_data.assigned_to and task_data.assigned_to == cur_user:
            return jsonify(error_response("Cannot assign task to yourself")), 400

        # Track which fields are being updated
        updated_fields = []

        # Update only the fields that are present in the request body
        if task_data.title and task_data.title != task.title:
            task.title = task_data.title
            updated_fields.append("title")
        if task_data.description and task_data.description != task.description:
            task.description = task_data.description
            updated_fields.append("description")
        if task_data.due_date and task_data.due_date != task.due_date:
            task.due_date = task_data.due_date
            updated_fields.append("due_date")
        if task_data.priority and task_data.priority != task.priority:
            task.priority = task_data.priority
            updated_fields.append("priority")
        if task_data.status and task_data.status != task.status:
            task.status = task_data.status
            updated_fields.append("status")
        if task_data.assigned_to and task_data.assigned_to != task.assigned_to:
            task.assigned_to = task_data.assigned_to
            updated_fields.append("assigned_to")

        # If no fields were updated, return an appropriate response
        if not updated_fields:
            return jsonify(error_response("No changes detected in the task")), 400

        # Commit the changes to the database
        db.session.commit()
        logger.info(f"Task  {task_id} was updated by  user  {cur_user}")
        # Return feedback on what was updated
        return jsonify(success_response("Task updated successfully", {"task_id": task.id, "updated_fields": updated_fields})), 200
    
    except ValidationError as e:
        logger.error(f"failed update  task  {task_id} by user {cur_user}")
        return jsonify(error_response("Validation error", details=[err['msg'] for err in e.errors()])), 400 

#================================================================================================================================#



#=======================================================DELETE  TASK ROUTE===============================================#

#need clearification here , i havent  implmented role ....as admin can delete all tasks 

@task_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@jwt_required()
def delete_task(task_id):
    try:
        # Get the current user from JWT
        cur_user = get_jwt_identity()

        # Fetch the task from the database
        task = Task.query.get(task_id)

        # If task does not exist, return error
        if not task:
            return jsonify(error_response("Task not found")), 404

        # Ensure the task is not being deleted by someone who is not the assigned user or creator
        if task.assigned_by != cur_user and task.assigned_to != cur_user:
            return jsonify(error_response("You are not authorized to delete this task")), 403

        # Delete the task
        db.session.delete(task)
        db.session.commit()
        logger.info(f"Task delted {task_id} by user {cur_user}")
        # Return success response
        return jsonify(success_response("Task deleted successfully", {"task_id": task.id})), 200
    
    except Exception as e:
        logger.error(f"failed to delete {task_id} by user {cur_user}")
        # Handle any unexpected errors
        return jsonify(error_response("An error occurred while deleting the task", details=str(e))), 500
    
#=======================================================================================================================#



#=======================================================GET MY TASK ROUTE===============================================#

@task_bp.route('/my_tasks', methods=['GET'])
@jwt_required()
def get_my_tasks():
    try:
        cur_user = get_jwt_identity()
        data = fetch_tasks(cur_user, filter_by='assigned_to')
        logger.info(f"tasks retrieved by  user  {cur_user}")
        return jsonify(success_response("My tasks fetched successfully", data)), 200
    except Exception as e:
        logger.error(f"failed  to  fetch tasks {str(e)} ")
        return jsonify(error_response("Failed to fetch tasks", details=str(e))), 500


@task_bp.route('/assigned_tasks', methods=['GET'])
@jwt_required()
def get_assigned_tasks():
    try:
        cur_user = get_jwt_identity()
        data = fetch_tasks(cur_user, filter_by='assigned_by')
        logger.info(f"tasks retrieved by  user  {cur_user}")
        return jsonify(success_response("Assigned tasks fetched successfully", data)), 200
    except Exception as e:
        logger.error(f"failed  to  fetch tasks {str(e)} ")
        return jsonify(error_response("Failed to fetch tasks", details=str(e))), 500



#=======================================================================================================================#




#=======================================================GET ASSINGED TASK ROUTE===============================================#

@task_bp.route('/get_task_by_id', methods=['GET'])
@jwt_required()
def get_task_by_id():
    try:
        cur_user = get_jwt_identity()
        task_id = request.args.get('task_id')

        if not task_id:
            return jsonify(error_response("Missing task_id parameter")), 400

        task = Task.query.filter_by(id=int(task_id)).first()

        if not task:
            return jsonify(error_response("Task not found")), 404

        # Optional: only allow if user is assigned or assigned_by
        if cur_user != task.assigned_to and cur_user != task.assigned_by:
            return jsonify(error_response("Unauthorized access to task")), 403

        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": str(task.due_date) if task.due_date else None,
            "priority": task.priority,
            "status": task.status,
            "assigned_to": task.assigned_to,
            "assigned_by": task.assigned_by
        }

        return jsonify(success_response("Task fetched successfully", task_data)), 200

    except Exception as e:
        return jsonify(error_response("Failed to fetch task", details=str(e))), 500
#=======================================================================================================================#