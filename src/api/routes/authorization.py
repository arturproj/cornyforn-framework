from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
router_bp_authorization = Blueprint('authorization', __name__)


@router_bp_authorization.post('/login')
def login():
    """POST /api/login
    Example route to log in a user and return JWT tokens.
    """
    # Here you would typically verify user credentials
    data = request.get_json()
    # For demonstration, we create a token for a user
    access_token = create_access_token(identity="user_id")
    refresh_token = create_refresh_token(identity="user_id")
    return jsonify(access_token=access_token, refresh_token=refresh_token), 201


@router_bp_authorization.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    """POST /api/refresh
    Example route to refresh the access token using a refresh token.
    Requires JWT authentication.
    """
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token), 200
    except:
        return jsonify({'message': 'Invalid token!'}), 403


# @router_bp_authorization.post('/logout')
# @jwt_required()
# def logout():
#     jti = get_jwt()["jti"]
#     jwt_blacklist = current_app.config.get('jwt_blacklist', set())
#     jwt_blacklist.add(jti)
#     current_app.config.update(jwt_blacklist=jwt_blacklist)
#     return jsonify({'message': "Token revoked"}), 200
