# 🧾 Task Management API - Backend Assessment

This is a **Task Management REST API** that allows users to register, login, create tasks, assign them to other users, and view/filter tasks. It is built with clean architecture, modular structure, and real-world features for user and task handling.

---

##Objective

Build a task tracking system that supports:
- User registration and login
- Task assignment between users
- Viewing tasks assigned *to* and *by* the user
- Task filtering by status, priority, date range
- Pagination and search
- View a task by ID and delete task by ID
-Log every actions to  database 
---

## Technologies Used & Why 

| Technology              | Why Used |
|------------------------|----------|
| **Flask**               | Lightweight, efficient, easy to structure APIs |
| **Flask-JWT-Extended**  | JWT-based secure authentication |
| **SQLAlchemy**          | ORM for safer and cleaner DB operations |
| **Flask-Migrate**       | Handles migrations with version control |
| **dotenv**              | For secure environment variable management |
| **SQLite/MySQL**        | Relational DB suited for structured data |
| **bcrypt**              | Secure password hashing |
| **Werkzeug**            | Used internally by Flask for password hashing/verification |
| **Pydantic**            | Used for data validation, ensuring clean input and output data, enforcing type safety |

---








## 🧪 Core API Features

| Feature                 | Endpoint                                | Method |
|------------------------|------------------------------------------|--------|
| Register User          | `/api/auth/register`                    | POST   |
| Login                  | `/api/auth/login`                       | POST   |
| Add Task               | `/api/add_task`                         | POST   |
| Tasks Assigned To Me   | `/api/my_tasks`                         | GET    |
| Tasks Assigned By Me   | `/api/assigned_tasks`                   | GET    |
| Get Task by ID         | `/api/get_task_by_id?task_id=<id>`      | GET    |
| Delete Task            | `/api/delete_task?task_id=<id>`         | GET    |



# API Response Structure

This document explains the structure of the API responses used in this project.

## 1. Success Response (200 OK)

```json
{
  "response": {
    "message": "Operation successful",
    "data": {
      // Data returned from the API (e.g., task details, user info, etc.)
    },
    "error": null
  },
  "status_code": 200
}

## 2. failed response 

{
  "response": {
    "message": "Error description",
    "data": null,
    "error": {
      "code": "error_code",
      "details": "Detailed explanation of the error"
    }
  },
  "status_code": 400
}

##3.pagination 

{
  "response": {
    "message": "Tasks fetched successfully",
    "data": {
      "tasks": [
        // List of tasks
      ],
      "pagination": {
        "page": 1,
        "page_size": 10,
        "total_items": 100,
        "total_pages": 10,
        "has_previous": false,
        "has_next": true
      }
    },
    "error": null
  },
  "status_code": 200
}



> All protected routes require the `Authorization: Bearer <access_token>` header
## 🧠 Code Design Highlights

- 🔐 Token-based authentication
- 🧱 Modular structure (auth, tasks, utils, config)
- 🧭 Search + Filter + Paginate support in list APIs
- 📡 Consistent response structure
- 💥 Logging to  databse and  Graceful error handling 
- 📦 DRY: Common filtering/pagination logic reused
- 

**Setup the Project

Unzip the Project File and Navigate to the Project Folder
Begin by unzipping the project file and then navigate into the project directory.

Install Dependencies
Install the required dependencies by running the command:
pip install -r requirements.txt.

Set Up Environment Variables
Create a .env file in the root directory of your project. Inside the file, add the necessary environment variables like the database URL and secret key. For example:

DATABASE_URL=sqlite:///your_database.db  # Replace with your actual database URL  
SECRET_KEY=your_secret_key_here

Initialize the Database
Once your environment variables are set up, run the Flask CLI command to initialize the database:
flask init-db.

Run Migrations
After initializing the database, you may need to apply any migrations to reflect model changes. You can do this by running:
flask migrate-db.

Upgrade the Database
To apply the changes made by the migrations, use the following command:
flask upgrade-db.

Seed the Database
Now, run the seed.py script to insert the initial data into the database.

Run the Flask Application
Finally, you can start the Flask application by running:
python run.py.
