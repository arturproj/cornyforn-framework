from flask import Blueprint, jsonify, request, url_for
from flask_jwt_extended import jwt_required

router_bp_other = Blueprint('other', __name__)

# Define your API routes here
@router_bp_other.route('/other', methods=['GET'])
def other_route():
    """GET /api/other/
    Other route that returns a simple message.
    """
    return jsonify({"message": "This is an other route."})

@router_bp_other.route('/other', methods=['POST'])
@jwt_required()
def create_other():
    """POST /api/other/
    Other route to create a new other resource.
    Requires JWT authentication.
    """
    data = request.get_json()
    return jsonify({"message": "Other created.", "data": data}), 201

@router_bp_other.route('/other/<int:id>', methods=['GET'])
@jwt_required()
def get_other(id):
    """GET /api/other/<id>          
    Other route to retrieve an other resource by ID.
    Requires JWT authentication.
    """
    return jsonify({"message": f"Retrieved other with id {id}."})

@router_bp_other.route('/other/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_other(id):
    """DELETE /api/other/<id>
    Other route to delete an other resource by ID.
    Requires JWT authentication.
    """
    return jsonify({"message": f"Deleted other with id {id}."})
