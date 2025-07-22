from flask import Blueprint, current_app, render_template

api = Blueprint('api', __name__ , url_prefix='/api')

@api.get('/')
def index():
    routes = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint in ['api.index']:
            continue
        routes.append({
            "url": str(rule),
            "methods": list(rule.methods),
            "endpoint": rule.endpoint,
        })
    return render_template("index.html", routes=routes)

from .routes.authorization import router_bp_authorization
api.register_blueprint(router_bp_authorization, url_prefix='/v1/auth')

from .routes.example import router_bp_example
api.register_blueprint(router_bp_example, url_prefix='/v1')

from .routes.other import router_bp_other
api.register_blueprint(router_bp_other, url_prefix='/v1')

