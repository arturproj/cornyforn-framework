from .controllers.example import router_bp_example
from .controllers.authorization import router_bp_authorization
from flask import Blueprint, current_app, render_template
from flask.views import View

api = Blueprint('api', __name__, url_prefix='/api')

api.register_blueprint(router_bp_authorization, url_prefix='/v1/auth')

api.register_blueprint(router_bp_example, url_prefix='/v1/examples')