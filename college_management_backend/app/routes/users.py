from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, abort
from ..models import User
from ..schemas import UserSchema
from ..auth import login_required, roles_required

blp = Blueprint("Users", "users", url_prefix="/users", description="Users management endpoints")


@blp.route("/me")
class Me(MethodView):
    @blp.response(200, UserSchema)
    @login_required
    def get(self):
        """Get current user profile."""
        uid = request.user["sub"]
        user = User.query.get(uid)
        if not user:
            abort(404, description="User not found")
        return user


@blp.route("/")
class UsersList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @roles_required("admin")
    def get(self):
        """List users (admin only)."""
        return User.query.order_by(User.id.desc()).all()
