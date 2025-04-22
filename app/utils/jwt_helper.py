
#FILE IS FOR FUTURE USE............


from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta

# Secret Key for JWT encoding
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

def create_jwt_token(user_id):
    expiration_time = timedelta(hours=1)  # token valid for 1 hour
    payload = {
        'sub': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + expiration_time
    }
    
    print("Creating token with payload:", payload)  # Debugging
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print("Generated token:", token)  # Debugging
    return token

def decode_jwt_token(token):
    try:
        print("Decoding token:", token)  # Debugging
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # Debugging
        return payload['sub']  # Return user ID (sub claim)
    except jwt.ExpiredSignatureError:
        print("Error: Token has expired")  # Debugging
        return None
    except jwt.InvalidTokenError as e:
        print("Error: Invalid token:", str(e))  # Debugging
        return None

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            print("Authorization header missing")  # Debugging
            return jsonify({"error": "Authorization header missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            print("Invalid Authorization header format")  # Debugging
            return jsonify({"error": "Invalid Authorization header"}), 401

        token = parts[1]

        print("Received Token:", token)  # Debugging
        user_id = decode_jwt_token(token)
        if not user_id:
            print("Invalid or expired token")  # Debugging
            return jsonify({"error": "Invalid or expired token"}), 401

        # Attach user_id to kwargs and pass to the route function
        return f(user_id=user_id, *args, **kwargs)
    return decorated_function
