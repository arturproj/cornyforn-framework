from .controllers.other import router_bp_other
from .controllers.example import router_bp_example
from .controllers.authorization import router_bp_authorization
from flask import Blueprint, current_app, render_template
from flask.views import View

api = Blueprint('api', __name__, url_prefix='/api')


class ApiListViewContoller(View):
    """Base class for other views."""

    def __init__(self, template):
        self.template = template

    def dispatch_request(self, *args, **kwargs):
        """Render the API index page with a list of routes."""

        items = [
            {
                "url": str(rule),
                "methods": list(rule.methods),
                "endpoint": rule.endpoint,
            } for rule in current_app.url_map.iter_rules()
            if rule.endpoint not in ['static', 'index', 'api.index']
        ]
        return render_template(self.template, routes=items)


api.add_url_rule(
    "/", view_func=ApiListViewContoller.as_view('index', template='api/index.html'),
)

api.register_blueprint(router_bp_authorization, url_prefix='/v1/auth')

api.register_blueprint(router_bp_example, url_prefix='/v1')

api.register_blueprint(router_bp_other, url_prefix='/v1')
