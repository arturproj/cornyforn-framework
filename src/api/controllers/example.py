from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.Example import Example
from datetime import datetime
from services.database import db

router_bp_example = Blueprint('example', __name__)

def active_examples_helper():
    """Return query scoped to non-deleted rows."""
    return db.session.query(Example).filter(Example.deletedAt.is_(None))

def desactive_examples_helper():
    """Return query scoped to soft-deleted rows."""
    return db.session.query(Example).filter(Example.deletedAt.isnot(None))

@router_bp_example.get('')
def get_examples():
    """
    Get all active examples with pagination
    ---
    tags:
      - Examples
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number for pagination
      - name: limit
        in: query
        type: integer
        default: 30
        description: Number of items per page
    responses:
      200:
        description: List of examples
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              message:
                type: string
              createdAt:
                type: string
                format: date-time
              updatedAt:
                type: string
                format: date-time
              deletedAt:
                type: string
                format: date-time
    """
    # setup pagination
    page = int(request.args.get('page', 1)) - 1
    limit = int(request.args.get('limit', 30))

    examples = active_examples_helper().offset(page * limit).limit(limit).all()
    return jsonify([e.as_dict() for e in examples]), 200


@router_bp_example.post('')
@jwt_required()
def create_example():
    """
    Create a new example
    ---
    tags:
      - Examples
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - message
          properties:
            message:
              type: string
              description: The message content for the example
    responses:
      201:
        description: Example created successfully
        schema:
          type: object
          properties:
            success:
              type: string
            data:
              type: object
      400:
        description: Missing required field
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Unauthorized - missing or invalid token
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
    """
    Get example by ID
    ---
    tags:
      - Examples
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Example ID
    responses:
      200:
        description: Example found
        schema:
          type: object
          properties:
            data:
              type: object
      404:
        description: Example not found
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Unauthorized - missing or invalid token
    """
    example = active_examples_helper().filter_by(id=id).first()
    if not example:
        return jsonify({"error": "Example not found."}), 404
    
    return jsonify({"data": example.as_dict()}), 200


@router_bp_example.put('/<int:id>')
@jwt_required()
def update_example(id: int):
    """
    Update example by ID
    ---
    tags:
      - Examples
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Example ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - message
          properties:
            message:
              type: string
              description: Updated message content
    responses:
      200:
        description: Example updated successfully
        schema:
          type: object
          properties:
            success:
              type: string
            data:
              type: object
      400:
        description: Invalid request - missing message field
      404:
        description: Example not found
      401:
        description: Unauthorized - missing or invalid token
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
    """
    Soft delete example by ID
    ---
    tags:
      - Examples
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Example ID
    responses:
      200:
        description: Example soft-deleted successfully
        schema:
          type: object
          properties:
            success:
              type: string
            data:
              type: object
      404:
        description: Example not found
      500:
        description: Error deleting example
      401:
        description: Unauthorized - missing or invalid token
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
