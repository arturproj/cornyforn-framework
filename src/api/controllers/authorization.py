from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from models.User import User
from services.database import db
import hashlib

router_bp_authorization = Blueprint('authorization', __name__)

@router_bp_authorization.post('/create')
def create_user():
    """
    Create a new User
    ---
    tags:
      - Authentication
    summary: Register a new user account
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Unique username for the user
            password:
              type: string
              description: Password for the user account
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
              msg:
                  type: string
                  description: Success message
      400:
        description: Missing required fields
        schema:
            type: object
            properties:
                error:
                    type: string
    """
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing 'username' or 'password' field."}), 400
    
    password = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
    user = User(username=data['username'], password=password)

    db.session.add(user)
    db.session.commit()
    # Here you would typically create the user in your database
    return jsonify({'msg': 'User created successfully'}), 201
                            
@router_bp_authorization.post('/login')
def login():
    """
    User login
    ---
    tags:
      - Authentication
    summary: Authenticate user and return JWT tokens
    description: Authenticate user with username and password, returning JWT access and refresh tokens
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Unique username for the user
            password:
              type: string
              description: Password for the user account
    responses:
      201:
        description: Login successful, tokens issued
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
      400:
        description: Missing required fields
        schema:
            type: object
            properties:
                error:
                    type: string
      401:
        description: Invalid username or password
        schema:
            type: object
            properties:
                error:
                    type: string
    """
    # Here you would typically verify user credentials
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing 'username' or 'password' field."}), 400
    
    password = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()

    user = db.session.query(User).filter_by(username=data['username'], password=password).first()
    if not user:
        return jsonify({"error": "Invalid username or password."}), 401

    # For demonstration, we create a token for a user
    access_token = create_access_token(identity=[user.id, user.username])
    refresh_token = create_refresh_token(identity=[user.id, user.username])
    return jsonify(access_token=access_token, refresh_token=refresh_token), 201


@router_bp_authorization.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    tags:
      - Authentication
    summary: Generate new access token using refresh token
    description: Generate a new access token using a valid refresh token
    security:
      - BearerAuth: []
    responses:
      200:
        description: New access token generated
        schema:
            type: object
            properties:
                access_token:
                    type: string
                    description: New JWT access token
      401:
        description: Invalid or expired refresh token
        schema:
            type: object
            properties:
                msg:
                    type: string
                    description: Error message
      403:
        description: Token validation failed
        schema:
            type: object
            properties:
                msg:
                    type: string
                    description: Error message
    """
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token), 200
    except:
        return jsonify({'msg': 'Invalid token!'}), 403


@router_bp_authorization.get('/logout')
@jwt_required()
def logout():
    """
    User logout
    ---
    tags:
      - Authentication
    summary: Revoke JWT token and logout user
    description: Revoke the current JWT token by adding it to the blacklist
    security:
      - BearerAuth: []
    responses:
      200:
        description: Token revoked successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  description: Logout confirmation message
      401:
        description: Invalid or missing token
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  description: Error message
    """
    jti = get_jwt()["jti"]
    jwt_blacklist = current_app.config.get('jwt_blacklist', set())
    jwt_blacklist.add(jti)
    current_app.config.update(jwt_blacklist=jwt_blacklist)
    return jsonify({'msg': "Token revoked"}), 200
