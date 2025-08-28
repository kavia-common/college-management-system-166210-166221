from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..extensions import db
from ..models import User
from ..schemas import LoginSchema, TokenSchema, UserCreateSchema, UserSchema
from ..token_utils import create_access_token

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="Authentication endpoints")


@blp.route("/login")
class Login(MethodView):
    """User login to obtain access token."""

    @blp.arguments(LoginSchema, location="json")
    @blp.response(200, TokenSchema)
    def post(self, args):
        """Login with email and password. Returns a bearer access token."""
        user = User.query.filter_by(email=args["email"]).first()
        if not user or not user.check_password(args["password"]) or not user.is_active:
            abort(401, description="Invalid credentials")
        token = create_access_token(user.id, user.role)
        return {"access_token": token, "token_type": "bearer"}


@blp.route("/register")
class Register(MethodView):
    """Register a new user (admin can also create other roles)."""

    @blp.arguments(UserCreateSchema, location="json")
    @blp.response(201, UserSchema)
    def post(self, args):
        """Create a user. For demo purpose, open registration; production should restrict by role."""
        if User.query.filter_by(email=args["email"]).first():
            abort(400, description="Email already registered")
        user = User(email=args["email"], name=args["name"], role=args["role"])
        user.set_password(args["password"])
        db.session.add(user)
        db.session.commit()
        return user
