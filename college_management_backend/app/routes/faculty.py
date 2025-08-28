from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..extensions import db
from ..models import Faculty, User
from ..schemas import FacultySchema
from ..auth import roles_required

blp = Blueprint("Faculty", "faculty", url_prefix="/faculty", description="Faculty management")


@blp.route("/")
class FacultyList(MethodView):
    @blp.response(200, FacultySchema(many=True))
    @roles_required("admin")
    def get(self):
        """List faculty (admin only)."""
        return Faculty.query.order_by(Faculty.id.desc()).all()

    @blp.arguments(FacultySchema, location="json")
    @blp.response(201, FacultySchema)
    @roles_required("admin")
    def post(self, args):
        """Create faculty profile."""
        user = User.query.get(args["user_id"])
        if not user:
            abort(404, description="User not found")
        if user.faculty_profile:
            abort(400, description="Faculty profile already exists for this user")
        f = Faculty(
            user_id=args["user_id"],
            employee_id=args["employee_id"],
            department=args["department"],
            designation=args.get("designation"),
        )
        db.session.add(f)
        db.session.commit()
        return f


@blp.route("/<int:faculty_id>")
class FacultyDetail(MethodView):
    @blp.response(200, FacultySchema)
    @roles_required("admin")
    def get(self, faculty_id: int):
        """Get faculty profile."""
        return Faculty.query.get_or_404(faculty_id)

    @blp.arguments(FacultySchema, location="json")
    @blp.response(200, FacultySchema)
    @roles_required("admin")
    def put(self, args, faculty_id: int):
        """Update faculty profile."""
        f = Faculty.query.get_or_404(faculty_id)
        for k in ["employee_id", "department", "designation"]:
            if k in args:
                setattr(f, k, args[k])
        db.session.commit()
        return f

    @roles_required("admin")
    def delete(self, faculty_id: int):
        """Delete faculty profile."""
        f = Faculty.query.get_or_404(faculty_id)
        db.session.delete(f)
        db.session.commit()
        return {"message": "Deleted"}
