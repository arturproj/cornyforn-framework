from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
router_bp_example = Blueprint('example', __name__, url_prefix='/example')

@router_bp_example.route('/example', methods=['GET'])
def example_route():
    """GET /api/example/
    Example route that returns a simple message.
    """
    return jsonify({"message": "This is an example route."})

@router_bp_example.route('/example', methods=['POST'])
@jwt_required()
def create_example():
    """POST /api/example/
    Example route to create a new example resource.
    Requires JWT authentication.
    """
    data = request.get_json()
    return jsonify({"message": "Example created.", "data": data}), 201

@router_bp_example.route('/example/<int:id>', methods=['GET'])
@jwt_required()
def get_example(id):
    """GET /api/example/<id>
    Example route to retrieve an example resource by ID.
    Requires JWT authentication.
    """
    return jsonify({"message": f"Retrieved example with id {id}."})

@router_bp_example.route('/example/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_example(id):
    """DELETE /api/example/<id>
    Example route to delete an example resource by ID.
    Requires JWT authentication.
    """
    return jsonify({"message": f"Deleted example with id {id}."})
