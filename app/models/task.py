from app.extensions import db
from datetime import datetime
from sqlalchemy import Enum

class TaskStatusEnum(db.Enum):
    OPEN = 1
    IN_PROGRESS = 2
    DONE = 3
    OVERDUE= 4

class PriorityEnum(db.Enum):
    LOW = 1
    HIGH = 2

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    overdue = db.Column(db.Boolean, default=False)
    
    priority = db.Column(db.Integer, nullable=False, default=1)  # 1 = Low, 2 = High
    status = db.Column(db.Integer, nullable=False, default=1)    # 1-4 enum

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   

    #i  just  crated the single refrence  

    
    # Foreign Keys
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_to = db.Column(db.Integer, nullable=False)  # New column for assigning tasks

    # Define the relationships explicitly with foreign_keys argument
    assigned_by_user = db.relationship('User', foreign_keys=[assigned_by], backref=db.backref('tasks_assigned_by', lazy='dynamic'))
    #assigned_to_user = db.relationship('User', foreign_keys=[assigned_to], backref=db.backref('tasks_assigned_to', lazy='dynamic'))

    def __repr__(self):
        return f'<Task {self.title} - Status {self.status} - Priority {self.priority}>'


