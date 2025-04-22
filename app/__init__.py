from flask import Flask,jsonify
from app.extensions import db, migrate
from app.config import Config
from app.routes.auth import auth_bp
from app.routes.task import task_bp 
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os
from dotenv import load_dotenv
load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_strong_secret_key')  
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')  # PLEASE SET YOUR KEY IN ENV, I M USING DEFAULT ON LOCAL

    app.config['SECRET_KEY'] =  SECRET_KEY 
    app.config["JWT_SECRET_KEY"] =  JWT_SECRET_KEY 
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    #add  custom response  for consistency in jwt  handling  ...


    
    @jwt.unauthorized_loader
    def custom_missing_auth_header(err_msg):
        return jsonify({
            "response": {
                "message": "Authentication required",
                "data": None,
                "error": {
                    "code": "auth_missing",
                    "details": err_msg
                }
            },
            "status_code": 401
        }), 401

    @jwt.invalid_token_loader
    def custom_invalid_token(err_msg):
        return jsonify({
            "response": {
                "message": "Invalid token",
                "data": None,
                "error": {
                    "code": "invalid_token",
                    "details": err_msg
                }
            },
            "status_code": 422
        }), 422

    @jwt.expired_token_loader
    def custom_expired_token(jwt_header, jwt_payload):
        return jsonify({
            "response": {
                "message": "Token expired",
                "data": None,
                "error": {
                    "code": "token_expired",
                    "details": "The token has expired"
                }
            },
            "status_code": 401
        }), 401

    # # Import models after app is created
    with app.app_context():
        from app.models import user, task  # Import models within app context

    # Register blueprints for routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(task_bp, url_prefix='/api')

    return app
