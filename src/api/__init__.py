from flask import Blueprint

api = Blueprint('api', __name__ , url_prefix='/api')

from .routes.authorization import router_bp_authorization
api.register_blueprint(router_bp_authorization, url_prefix='/v1/auth')

from .routes.example import router_bp_example
api.register_blueprint(router_bp_example, url_prefix='/v1')

from .routes.other import router_bp_other
api.register_blueprint(router_bp_other, url_prefix='/v1')

