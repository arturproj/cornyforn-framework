import os
from flask import redirect, url_for
# from api.controllers import example
# from api.controllers.example import router_bp_example
from dotenv import load_dotenv
# Import the database instance
from services.database import db
# Create the Flask application
# It can be used to set the name of the application in the Flask context
from services.application import create_app

# Load environment variables from .env file
# Load the base .env file first
load_dotenv()

# Conditionally load .env.local for development or .env.prod for production
APP_ENVIRONMENT = os.getenv("APP_DEBUG") == "True"

if APP_ENVIRONMENT:
    load_dotenv('.env.local', override=True)
else:
    load_dotenv('.env.prod', override=True)

app = create_app(__name__)
# Initialize the database
db.init_app(app)  # Initialize SQLAlchemy with the Flask app

@app.route('/')
def index():
    return redirect(url_for('api.index'))  # Redirect to the API index page

# Run the application
if __name__ == "__main__":
    with app.app_context():
        # Create all tables in the database
        db.create_all()

    app.run(debug=True)
