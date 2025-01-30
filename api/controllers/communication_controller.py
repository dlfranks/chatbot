from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.communication import Communication
from api import db

communication_bp = Blueprint('communication_bp', __name__)

@communication_bp.route('/communications', methods=['GET'])
#@jwt_required()
def get_communications():
    try:
        #user_identity = get_jwt_identity()
        #print(f"Authenticated user: {user_identity}")  # Log the authenticated user
        communications = Communication.query.all()
        return jsonify([comm.to_dict() for comm in communications])
    except Exception as e:
        print(f"Error in get_communications: {str(e)}")
        raise Exception("Intentional error for testing.")
        

@communication_bp.route('/communications/<int:comm_id>', methods=['GET'])
def get_communication_by_id(comm_id):
    communication = Communication.query.get(comm_id)
    if communication:
        return jsonify(communication.to_dict())
    return "Communication not found", 404

@communication_bp.route('/communications', methods=['POST'])
def create_communication():
    data = request.json
    new_communication = Communication(**data)
    db.session.add(new_communication)
    db.session.commit()
    return "Communication created successfully", 201

@communication_bp.route('/communications/<int:comm_id>', methods=['PUT'])
def update_communication(comm_id):
    communication = Communication.query.get(comm_id)
    if not communication:
        return "Communication not found", 404
    data = request.json
    for key, value in data.items():
        setattr(communication, key, value)
    db.session.commit()
    return "Communication updated successfully"

@communication_bp.route('/communications/<int:comm_id>', methods=['DELETE'])
def delete_communication(comm_id):
    communication = Communication.query.get(comm_id)
    if not communication:
        return "Communication not found", 404
    db.session.delete(communication)
    db.session.commit()
    return "Communication deleted successfully"