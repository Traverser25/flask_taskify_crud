# app/utils/response_util.py

def success_response(message: str, data=None, status_code=200):
    return {
        "response": {
            "message": message,
            "data": data,
            "error": None
        },
        "status_code": status_code
    }

def error_response(message: str, error=None, status_code=400):
    return {
        "response": {
            "message": message,
            "data": None,
            "error": error
        },
        "status_code": status_code
    }
