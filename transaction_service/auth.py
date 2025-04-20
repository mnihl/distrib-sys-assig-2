from functools import wraps
from flask import request, jsonify

# Dummy in-memory token store for demo
TOKENS = {
    "admin-token": {"role": "administrator"},
    "agent-token": {"role": "agent"},
    "secretary-token": {"role": "secretary"},
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token not in TOKENS:
            return jsonify({"error": "Unauthorized"}), 401
        request.user = TOKENS[token]
        return f(*args, **kwargs)
    return decorated

def roles_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(request, 'user', None)
            if user is None or user['role'] not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
