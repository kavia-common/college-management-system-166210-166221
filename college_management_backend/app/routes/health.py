from flask_smorest import Blueprint
from flask.views import MethodView

# Fix tag/name spelling and keep url_prefix rooted
blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    """Simple liveness probe."""
    def get(self):
        """Returns Healthy message for liveness check."""
        return {"message": "Healthy"}
