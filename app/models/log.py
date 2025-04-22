from app.extensions import db
from datetime import datetime

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(50), nullable=False)  # e.g., INFO, ERROR
    message = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100))  # optional: which route/function
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
