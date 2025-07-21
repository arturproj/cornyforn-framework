from flask import Flask, render_template, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from api import api
# from api.routes import example
# from api.routes.example import router_bp_example

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

import os

load_dotenv() # Load environment variables from .env file
def create_app():
        app = Flask(__name__)

    # Load configuration from a config file or environment variables
        app.config.from_mapping(
            SECRET_KEY='your_secret_key',
            JWT_SECRET_KEY='your_jwt_secret_key',  # Change this to a secure key
            JWT_ACCESS_TOKEN_EXPIRES=3600,  # Token expiration time in seconds
            # Add other configurations here
        )
        # Initialize JWT Manager
        JWTManager(app)
        
        @app.route('/login', methods=['POST'])
        def login():
            #
            # More complex login logic would go here
            #
            # For demonstration, we create a token for a user
            access_token = create_access_token(identity="user_id")
            return jsonify(access_token=access_token), 201

    # Register the APIs blueprint    
        app.register_blueprint(api)
        
        # Additional example routes can be registered here if needed
        # Uncomment one of the following lines to register example routes

        # Method 1: Register the example routes directly using the blueprint
        ### Uncomment to register example routes directly
        # app.register_blueprint(example.router_bp_example, url_prefix='/api')

        # Method 2: Register the example routes using the blueprint
        ### Uncomment to register example routes using the blueprint
        # app.register_blueprint(router_bp_example, url_prefix='/api')

        return app


app = create_app()


@app.route('/')
def index():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "url": str(rule),
            "methods": list(rule.methods),
            "endpoint": rule.endpoint,
        })
    return render_template("index.html", routes=routes)


if __name__ == "__main__":
    app.run(debug=True)
