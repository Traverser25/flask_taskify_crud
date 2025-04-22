import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking (optional)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/prg_tasks_db')  # Fetch from .env, or default to local MySQL URI
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_strong_secret_key')  # Fetch from .env, or default value
