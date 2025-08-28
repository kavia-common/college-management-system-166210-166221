from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..extensions import db
from ..models import Grade, Student, Course
from ..schemas import GradeSchema
from ..auth import roles_required

blp = Blueprint("Grades", "grades", url_prefix="/grades", description="Grades and results management")


@blp.route("/")
class GradeList(MethodView):
    @blp.response(200, GradeSchema(many=True))
    @roles_required("admin", "faculty", "student")
    def get(self):
        """List grades."""
        return Grade.query.order_by(Grade.id.desc()).all()

    @blp.arguments(GradeSchema, location="json")
    @blp.response(201, GradeSchema)
    @roles_required("admin", "faculty")
    def post(self, args):
        """Assign a grade to a student in a course."""
        _ = Student.query.get(args["student_id"]) or abort(404, description="Student not found")
        _ = Course.query.get(args["course_id"]) or abort(404, description="Course not found")
        existing = Grade.query.filter_by(course_id=args["course_id"], student_id=args["student_id"]).first()
        if existing:
            abort(400, description="Grade already exists for this student in the course")
        g = Grade(course_id=args["course_id"], student_id=args["student_id"], grade=args["grade"])
        db.session.add(g)
        db.session.commit()
        return g


@blp.route("/<int:grade_id>")
class GradeDetail(MethodView):
    @blp.response(200, GradeSchema)
    @roles_required("admin", "faculty", "student")
    def get(self, grade_id: int):
        """Get a grade record."""
        return Grade.query.get_or_404(grade_id)

    @blp.arguments(GradeSchema, location="json")
    @blp.response(200, GradeSchema)
    @roles_required("admin", "faculty")
    def put(self, args, grade_id: int):
        """Update grade value."""
        g = Grade.query.get_or_404(grade_id)
        if "grade" in args:
            g.grade = args["grade"]
        db.session.commit()
        return g

    @roles_required("admin")
    def delete(self, grade_id: int):
        """Delete grade record."""
        g = Grade.query.get_or_404(grade_id)
        db.session.delete(g)
        db.session.commit()
        return {"message": "Deleted"}
