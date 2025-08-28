from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..extensions import db
from ..models import Course, Faculty
from ..schemas import CourseSchema
from ..auth import roles_required

blp = Blueprint("Courses", "courses", url_prefix="/courses", description="Course management")


@blp.route("/")
class CourseList(MethodView):
    @blp.response(200, CourseSchema(many=True))
    @roles_required("admin", "faculty", "student")
    def get(self):
        """List courses."""
        return Course.query.order_by(Course.id.desc()).all()

    @blp.arguments(CourseSchema, location="json")
    @blp.response(201, CourseSchema)
    @roles_required("admin")
    def post(self, args):
        """Create course (admin only)."""
        faculty_id = args.get("faculty_id")
        if faculty_id:
            _ = Faculty.query.get(faculty_id) or abort(404, description="Faculty not found")
        c = Course(
            code=args["code"],
            title=args["title"],
            credits=args["credits"],
            faculty_id=faculty_id,
        )
        db.session.add(c)
        db.session.commit()
        return c


@blp.route("/<int:course_id>")
class CourseDetail(MethodView):
    @blp.response(200, CourseSchema)
    @roles_required("admin", "faculty", "student")
    def get(self, course_id: int):
        """Get a course."""
        return Course.query.get_or_404(course_id)

    @blp.arguments(CourseSchema, location="json")
    @blp.response(200, CourseSchema)
    @roles_required("admin")
    def put(self, args, course_id: int):
        """Update a course (admin only)."""
        c = Course.query.get_or_404(course_id)
        for k in ["code", "title", "credits", "faculty_id"]:
            if k in args:
                if k == "faculty_id" and args[k] is not None:
                    _ = Faculty.query.get(args[k]) or abort(404, description="Faculty not found")
                setattr(c, k, args[k])
        db.session.commit()
        return c

    @roles_required("admin")
    def delete(self, course_id: int):
        """Delete a course (admin only)."""
        c = Course.query.get_or_404(course_id)
        db.session.delete(c)
        db.session.commit()
        return {"message": "Deleted"}
