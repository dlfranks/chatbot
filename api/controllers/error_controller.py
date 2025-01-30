from flask import Blueprint, jsonify, request

error_bp = Blueprint('error_bp', __name__)

@error_bp.route('/cause-error', methods=['GET'])
def cause_error():
    raise Exception("Intentional error for testing.")