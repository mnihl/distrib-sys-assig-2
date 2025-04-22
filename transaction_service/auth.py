import requests
from functools import wraps
from flask import request, jsonify

def verify_token_external(token):
    try:
        response = requests.post(
            "http://localhost:5000/verify",
            json={"token": token}
        )
        return response.status_code == 200
    except:
        return False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not verify_token_external(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

def roles_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"error": "Unauthorized"}), 401

            role = token.split(":")[0].lower()
            if role not in [r.lower() for r in allowed_roles]:
                return jsonify({"error": "Forbidden"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
