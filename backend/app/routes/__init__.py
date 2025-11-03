from .tasks import tasks_bp
from .users import users_bp
from .health import health_bp

def register_blueprints(app):
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(health_bp, url_prefix="/api/health")
