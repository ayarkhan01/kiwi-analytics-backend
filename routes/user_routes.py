from flask import Blueprint, request, jsonify, session
from services.user_dao import password_match, get_user_id, create_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
        
    if password_match(username, password):
        user_id = get_user_id(username)
        # You might want to use a proper session or JWT token here
        return jsonify({"user_id": user_id, "message": "Login successful"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@user_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    try:
        user_id = create_user(username, password)
        return jsonify({"user_id": user_id, "message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500