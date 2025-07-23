from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from models.Example import Example
from datetime import datetime
router_bp_example = Blueprint('example', __name__)


@router_bp_example.get('/examples')
def example_route():
    """GET /api/v1/examples/
    Example route to retrieve a list of examples.
    This route does not require authentication.
    It returns a list of example resources in JSON format.
    """
    serialized = [item.as_dict() for item in Example.query.all()]
    return jsonify(serialized), 200


@router_bp_example.post('/examples')
@jwt_required()
def create_example():
    """POST /api/v1/examples/
    Example route to create a new example resource.
    Requires JWT authentication.
    """
    data = request.get_json()
    if 'message' not in data:
        return jsonify({"msg": "Missing 'message' field."}), 400
    
    new_example = Example(message=data['message'])

    current_app.extensions['sqlalchemy'].session.add(new_example)
    current_app.extensions['sqlalchemy'].session.commit()
    current_app.extensions['sqlalchemy'].session.refresh(new_example)

    return jsonify({"msg": "Example created.", "data": new_example.as_dict()}), 201


@router_bp_example.get('/example/<int:id>')
@jwt_required()
def get_example(id: int):
    """GET /api/v1/example/<id>
    Example route to retrieve an example resource by ID.
    Requires JWT authentication.
    """
    example = Example.query.get(id)
    if not example:
        return jsonify({"msg": "Example not found."}), 404
    serialized = example.as_dict()
    return jsonify(serialized), 200


@router_bp_example.put('/example/<int:id>')
@jwt_required()
def update_example(id: int):
    """PUT /api/v1/example/<id>
    Example route to update an example resource by ID.
    Requires JWT authentication.
    """
    example = Example.query.get(id)
    if not example:
        return jsonify({"msg": "Example not found."}), 404

    data = request.get_json()
    if 'message' in data:
        example.message = data['message']

    current_app.extensions['sqlalchemy'].session.commit()
    current_app.extensions['sqlalchemy'].session.refresh(example)

    return jsonify({"msg": "Example updated.", "data": example.as_dict()}), 200


@router_bp_example.delete('/example/<int:id>')
@jwt_required()
def soft_delete_example(id: int):
    """DELETE /api/v1/example/<id>
    Example route to delete an example resource by ID.
    Requires JWT authentication.
    """
    example = Example.query.get(id)
    if not example:
        return jsonify({"msg": "Example not found."}), 404

    example.deletedAt = datetime.now()  # Soft delete

    current_app.extensions['sqlalchemy'].session.commit()
    current_app.extensions['sqlalchemy'].session.refresh(example)

    if example.deletedAt:
        return jsonify({"msg": "Example soft-deleted.", "data": example.as_dict()}), 200
    else:
        return jsonify({"msg": "Example not soft-deleted."}), 500


@router_bp_example.delete('/example/<int:id>/prune')
@jwt_required()
def delete_example_permanently(id: int):
    """DELETE /api/v1/example/<id>/prune
    Example route to delete an example resource by ID.
    Requires JWT authentication.
    """
    example = Example.query.get(id)
    if not example:
        return jsonify({"msg": "Example not found."}), 404

    current_app.extensions['sqlalchemy'].session.delete(example)
    current_app.extensions['sqlalchemy'].session.commit()

    return jsonify({"msg": "Example permanently deleted."}), 200
