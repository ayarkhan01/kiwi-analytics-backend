from functools import wraps
from flask import request, jsonify, g
from services.user_dao import get_user_id

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 401
        
        # This is a simple authentication check
        # In a real app, you would validate a JWT token or session
        try:
            # Assuming auth_header is "Bearer user_id"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({"error": "Invalid authorization format"}), 401
                
            user_id = int(parts[1])
            g.user_id = user_id  # Store in Flask's g object for the request
        except:
            return jsonify({"error": "Invalid authorization token"}), 401
            
        return f(*args, **kwargs)
    return decorated_function