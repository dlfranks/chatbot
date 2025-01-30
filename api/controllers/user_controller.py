from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.user import User
from api import db

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate email and password presence
    errors = {}
    if not email:
        errors['email'] = 'Email is required.'
    if not password:
        errors['password'] = 'Password is required.'

    if errors:
        return jsonify({'errors': errors}), 400

    # Validate email and password
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Authenticate user
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate JWT token
    token = user.generate_token()
    return jsonify({'message': 'Login successful', 'token': token}), 200

@user_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')

    # Validate email and new_password presence
    errors = {}
    if not email:
        errors['email'] = 'Email is required.'
    if not new_password:
        errors['new_password'] = 'New password is required.'

    if errors:
        return jsonify({'errors': errors}), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'errors': {'email': 'User with this email does not exist.'}}), 404

    # Update password
    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password reset successfully.'}), 200

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return "User not found", 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    raw_password = data.pop('password')
    new_user = User(**data)
    new_user.set_password(raw_password)
    db.session.add(new_user)
    db.session.commit()
    return "User created successfully", 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    data = request.json
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return "User updated successfully"

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    db.session.delete(user)
    db.session.commit()
    return "User deleted successfully"