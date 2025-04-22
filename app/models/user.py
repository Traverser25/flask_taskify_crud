from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    #later  will verify with  pydantic 

    # tasks = db.relationship('Task', backref='user', lazy=True)

      
    # tasks_assigned_by = db.relationship('Task', backref='assigned_by_user', foreign_keys='Task.assigned_by', lazy=True)
    # tasks_assigned_to = db.relationship('Task', backref='assigned_to_user', foreign_keys='Task.assigned_to', lazy=True)


    # # tasks_assigned_by = db.relationship(
    # #     'Task',
    # #     foreign_keys='Task.assigned_by',
    # #     backref=db.backref('assigned_by_user', lazy='dynamic'),
    # #     overlaps="tasks,user",  
    # #     lazy=True
    # # )


    def __repr__(self):
        return f'<User {self.username}>'
