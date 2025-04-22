from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
import jwt
from datetime import datetime, timedelta
import re  
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app.utils.jwt_helper import create_jwt_token

from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from app.utils.api_response import success_response,error_response

auth_bp = Blueprint('auth', __name__)


email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    username=data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        res = error_response("login failed", "email and password are required", 400)
        return jsonify(res["response"]), res["status_code"]
    
    # Validate email format
    if not re.match(email_regex, email):
       res = error_response("login failed", "invalid  email ", 400)
       return jsonify(res["response"]), res["status_code"]
    
    # Check if the user already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        res = error_response("Registration failed", "User already exists", 400)
        return jsonify(res["response"]), res["status_code"]
    
    
    hashed_password = generate_password_hash(password)

    # Create new user
    new_user = User(username=username,email=email, password_hash=hashed_password)

    try:
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        res = success_response("login succesful", "User registred successfully",201)
        return jsonify(res["response"]), res["status_code"]
    except Exception as e:
        db.session.rollback()
        print(e)
        res = error_response("Registration failed", f"Error creating user: {str(e)}", 500)
        return jsonify(res["response"]), res["status_code"]
       
    


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

   
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        res = error_response("login failed", "email and password are required", 400)
        return jsonify(res["response"]), res["status_code"]
        
    
    # Find the user in the database
    user = User.query.filter_by(email=email).first()
    if not user:
        res = error_response("login failed", "Invalid email or password", 401)
        return jsonify(res["response"]), res["status_code"]
        #return jsonify({"error": "Invalid email or password"}), 401

    # Check if the provided password matches the hashed password
    if not check_password_hash(user.password_hash, password):
        res = error_response("login failed", "Invalid email or password", 401)
        return jsonify(res["response"]), res["status_code"]
       

    # Generate JWT token
    token =create_access_token(identity=user.id)
    res = success_response("login succesful", {"token": token}, 200)
    return jsonify(res["response"]), res["status_code"]

