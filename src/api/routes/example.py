from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
router_bp_example = Blueprint('example', __name__, url_prefix='/example')

@router_bp_example.get('/example')
def example_route():
    """GET /api/v1/example/
    Example route that returns a simple msg.
    """
    return jsonify({"msg": "This is an example route."})

@router_bp_example.post('/example')
@jwt_required()
def create_example():
    """POST /api/v1/example/
    Example route to create a new example resource.
    Requires JWT authentication.
    """
    data = request.get_json()
    return jsonify({"msg": "Example created.", "data": data}), 201

@router_bp_example.get('/example/<int:id>')
@jwt_required()
def get_example(id: int):
    """GET /api/v1/example/<id>
    Example route to retrieve an example resource by ID.
    Requires JWT authentication.
    """
    # In a real application, you would fetch the resource from the database
    # Here we just return a dummy response
    return jsonify({"msg": f"Retrieved example with id {id}."})

@router_bp_example.delete('/example/<int:id>')
@jwt_required()
def delete_example(id: int):
    """DELETE /api/v1/example/<id>
    Example route to delete an example resource by ID.
    Requires JWT authentication.
    """
    return jsonify({"msg": f"Deleted example with id {id}."})
