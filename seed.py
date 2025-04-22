from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.task import Task
from app import create_app
from werkzeug.security import generate_password_hash
from app.utils.logger import logger

print("App context added")

app = create_app()

with app.app_context():
    #

    # Add sample users with hashed passwords
    users = [
        {"username": "admin_user", "email": "admin@example.com", "password": "admin123"},
        {"username": "john_doe", "email": "john@example.com", "password": "john123"},
        {"username": "jane_smith", "email": "jane@example.com", "password": "jane123"}
    ]

    for user_data in users:
        # Hash the password using Werkzeug's generate_password_hash
        hashed_password = generate_password_hash(user_data["password"])

        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=hashed_password  # Store the hashed password
        )
        db.session.add(user)
    
    db.session.commit()

    print("Users added successfully with hashed passwords")
