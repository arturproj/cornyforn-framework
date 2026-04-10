from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from models.User import User
from services.database import db
import hashlib

from flasgger import swag_from

router_bp_authorization = Blueprint('authorization', __name__)

@router_bp_authorization.route('/create',methods=['POST'])
@swag_from('docs/user/create_user.yaml')
def create_user():
    """POST /api/v1/auth/create
    Create a new user account.
    This route accepts a JSON payload with 'username' and 'password' fields.
    It creates a new user in the database with the provided credentials.
    """
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing 'username' or 'password' field."}), 400
    
    password = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
    user = User(username=data['username'], password=password)

    db.session.add(user)
    db.session.commit()
    # Here you would typically create the user in your database
    return jsonify({'success': 'User created successfully'}), 201
                            
@router_bp_authorization.route('/login', methods=['POST'])
@swag_from('docs/authorization/login_user.yaml')
def login():
    """POST /api/v1/auth/login
    User login to obtain JWT tokens.
    This route accepts a JSON payload with 'username' and 'password' fields.
    It verifies the credentials and returns an access token and a refresh token if valid.
    Otherwise, it returns an error message.
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
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 201


@router_bp_authorization.post('/refresh')
@jwt_required(refresh=True)
@swag_from('docs/authorization/refresh_token.yaml')
def refresh():
    """POST /api/v1/auth/refresh
    Refresh the access token using a valid refresh token.
    This route requires a valid refresh token and will return a new access token.
    """
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token), 200
    except:
        return jsonify({'msg': 'Invalid token!'}), 403


@router_bp_authorization.route('/logout', methods=['GET'])
@jwt_required()
@swag_from('docs/authorization/logout_user.yaml')
def logout():
    """GET /api/v1/auth/logout
    User logout by revoking the current JWT token.
    This route requires JWT authentication and will add the token's JTI to the blacklist.
    """
    jti = get_jwt()["jti"]
    jwt_blacklist = current_app.config.get('jwt_blacklist', set())
    jwt_blacklist.add(jti)
    current_app.config.update(jwt_blacklist=jwt_blacklist)
    return jsonify({'success': True, "message": "Token revoked"}), 200
