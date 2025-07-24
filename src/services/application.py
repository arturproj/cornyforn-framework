import os
from flask import Flask
from flask_jwt_extended import JWTManager
from api import api
from datetime import timedelta


def create_app(namespace=__name__):
    app = Flask(namespace)

# Load configuration from a config file or environment variables
    app.config.from_mapping(
        DEBUG=os.getenv('APP_DEBUG', True),  # Set to True for development
        TESTING=os.getenv('APP_TESTING', False),  # Set to True for testing
        # Change this to a secure key
        SECRET_KEY=os.getenv('SECRET_KEY', 'your_secret_key'),
        # Change this to a secure key
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key'),
        # Token expiration time in seconds
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(seconds=int(
            os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))),
        JWT_BLACKLIST_ENABLED=os.getenv(
            'JWT_BLACKLIST_ENABLED', True),
        # Token checks
        JWT_BLACKLIST_TOKEN_CHECKS=os.getenv(
            'JWT_BLACKLIST_TOKEN_CHECKS', [
                # 'access' and 'refresh' are the default checks
                'access', 'refresh'
            ]),
        # Refresh token expiration time in seconds
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(seconds=int(os.getenv(
            'JWT_REFRESH_TOKEN_EXPIRES', 86400))),        # Enable token blacklist

        SQLALCHEMY_DATABASE_URI=os.getenv(
            'SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://localhost:3306/test'),
        # Add other configurations here
        # ... e.g., etc.
    )

    # Initialize JWT Manager
    jwt = JWTManager(app)
    # Make blacklist available in the app context
    app.config['jwt_blacklist'] = set()

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Check if the token is revoked."""
        # The 'jti' (JWT ID) is a unique identifier for the token
        # You can store revoked tokens in a database or in-memory set
        # Here we use an in-memory set for simplicity
        # In a real application, you would check against a persistent store
        jti = jwt_payload["jti"]
        # Check if the token ID is in the blacklist
        return jti in app.config['jwt_blacklist']

# Register the APIs blueprint
    app.register_blueprint(api)

    # Additional example controllers can be registered here if needed
    # Uncomment one of the following lines to register example controllers

    # Method 1: Register the example controllers directly using the blueprint
    # Uncomment to register example controllers directly
    # app.register_blueprint(example.router_bp_example, url_prefix='/api')

    # Method 2: Register the example controllers using the blueprint
    # Uncomment to register example controllers using the blueprint
    # app.register_blueprint(router_bp_example, url_prefix='/api')

    return app
