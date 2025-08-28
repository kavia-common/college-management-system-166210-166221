from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort, request
from ..extensions import db
from ..models import Student, User
from ..schemas import StudentSchema
from ..auth import roles_required

blp = Blueprint("Students", "students", url_prefix="/students", description="Student registration and profiles")


@blp.route("/")
class StudentList(MethodView):
    @blp.response(200, StudentSchema(many=True))
    @roles_required("admin", "faculty")
    def get(self):
        """List students."""
        return Student.query.order_by(Student.id.desc()).all()

    @blp.arguments(StudentSchema, location="json")
    @blp.response(201, StudentSchema)
    @roles_required("admin")
    def post(self, args):
        """Create student profile for a user."""
        user = User.query.get(args["user_id"])
        if not user:
            abort(404, description="User not found")
        if user.student_profile:
            abort(400, description="Student profile already exists for this user")
        s = Student(
            user_id=args["user_id"],
            roll_number=args["roll_number"],
            department=args["department"],
            year=args["year"],
        )
        db.session.add(s)
        db.session.commit()
        return s


@blp.route("/<int:student_id>")
class StudentDetail(MethodView):
    @blp.response(200, StudentSchema)
    @roles_required("admin", "faculty", "student")
    def get(self, student_id: int):
        """Get a student's profile; student can only get their own."""
        s = Student.query.get_or_404(student_id)
        payload = request.user
        if payload["role"] == "student" and s.user_id != payload["sub"]:
            abort(403, description="Forbidden")
        return s

    @blp.arguments(StudentSchema, location="json")
    @blp.response(200, StudentSchema)
    @roles_required("admin")
    def put(self, args, student_id: int):
        """Update student profile (admin only)."""
        s = Student.query.get_or_404(student_id)
        for k in ["roll_number", "department", "year"]:
            if k in args:
                setattr(s, k, args[k])
        db.session.commit()
        return s

    @roles_required("admin")
    def delete(self, student_id: int):
        """Delete student profile (admin only)."""
        s = Student.query.get_or_404(student_id)
        db.session.delete(s)
        db.session.commit()
        return {"message": "Deleted"}
