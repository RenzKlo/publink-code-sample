from functools import wraps
from flask import jsonify
import logging


def handle_errors(f):
    """Decorator to handle common errors in route handlers."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(f"An error occurred in {f.__name__}: {e}")
            return jsonify({"error": "An error occurred", "message": str(e)}), 500
    return decorated_function


def validate_required_fields(required_fields):
    """Decorator to validate required fields in request data."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is required"}), 400
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
