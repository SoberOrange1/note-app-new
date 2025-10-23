from flask import Blueprint, jsonify, request
from src.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = User.find_all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.json
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Username and email are required'}), 400
        
        # Check if username or email already exists
        if User.find_by_username(data['username']):
            return jsonify({'error': 'Username already exists'}), 400
        if User.find_by_email(data['email']):
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(username=data['username'], email=data['email'])
        user.save()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a specific user"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check for duplicate username/email if being changed
        if 'username' in data and data['username'] != user.username:
            if User.find_by_username(data['username']):
                return jsonify({'error': 'Username already exists'}), 400
                
        if 'email' in data and data['email'] != user.email:
            if User.find_by_email(data['email']):
                return jsonify({'error': 'Email already exists'}), 400
        
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.save()
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a specific user"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        user.delete()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
