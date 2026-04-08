from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.Example import Example
from datetime import datetime
from services.database import db

router_bp_example = Blueprint('example', __name__)

def active_examples_helper():
    """Return query scoped to non-deleted rows."""
    return Example.query.filter(Example.deletedAt.is_(None))

def desactive_examples_helper():
    """Return query scoped to soft-deleted rows."""
    return Example.query.filter(Example.deletedAt.isnot(None))

@router_bp_example.get('/')
def get_examples():
    """GET /api/v1/examples/
    Example route to retrieve a list of examples.
    This route does not require authentication.
    It returns a list of example resources in JSON format.
    """
    # setup pagination
    page = int(request.args.get('page', 1)) - 1
    limit = int(request.args.get('limit', 30))

    examples = active_examples_helper().offset(page * limit).limit(limit).all()
    return jsonify([e.as_dict() for e in examples]), 200


@router_bp_example.post('/')
@jwt_required()
def create_example():
    """POST /api/v1/examples/
    Example route to create a new example resource.
    Requires JWT authentication.
    """
    data = request.get_json()
    if 'message' not in data:
        return jsonify({"error": "Missing 'message' field."}), 400
    
    new_example = Example(message=data['message'])

    db.session.add(new_example)
    db.session.commit()

    return jsonify({"success": "Example created.", "data": new_example.as_dict()}), 201


@router_bp_example.get('/<int:id>')
@jwt_required()
def get_example(id: int):
    """GET /api/v1/examples/<id>
    Example route to retrieve an example resource by ID.
    Requires JWT authentication.
    """
    example = active_examples_helper().filter_by(id=id).first()
    if not example:
        return jsonify({"error": "Example not found."}), 404
    
    return jsonify({"data": example.as_dict()}), 200


@router_bp_example.put('/<int:id>')
@jwt_required()
def update_example(id: int):
    """PUT /api/v1/examples/<id>
    Example route to update an example resource by ID.
    Requires JWT authentication.
    """
    example = active_examples_helper().filter_by(id=id).first()
    if not example:
        return jsonify({"error": "Example not found."}), 404

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "'message' field is required"}), 400
    
    example.message = data['message']
    db.session.commit()

    return jsonify({"success": "Example updated.", "data": example.as_dict()}), 200


@router_bp_example.delete('/<int:id>')
@jwt_required()
def soft_delete_example(id: int):
    """DELETE /api/v1/examples/<id>
    Example route to delete an example resource by ID.
    Requires JWT authentication.
    """
    example = active_examples_helper().filter_by(id=id).first()
    if not example:
        return jsonify({"error": "Example not found."}), 404

    example.deletedAt = datetime.now()  # Soft delete
    db.session.commit()

    if example.deletedAt:
        return jsonify({"success": "Example soft-deleted.", "data": example.as_dict()}), 200
    else:
        return jsonify({"error": "Example not soft-deleted."}), 500


@router_bp_example.delete('/<int:id>/prune')
@jwt_required()
def delete_example_permanently(id: int):
    """DELETE /api/v1/examples/<id>/prune
    Example route to delete an example resource by ID.
    Requires JWT authentication.
    """
    example = desactive_examples_helper().filter_by(id=id).first()
    if not example:
        return jsonify({"error": "Example not found."}), 404

    db.session.delete(example)
    db.session.commit()

    return jsonify({"sucess": "Example permanently deleted."}), 200
