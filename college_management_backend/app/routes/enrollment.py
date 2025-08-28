from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..extensions import db
from ..models import Enrollment, Student, Course
from ..schemas import EnrollmentSchema
from ..auth import roles_required

blp = Blueprint("Enrollment", "enrollment", url_prefix="/enrollments", description="Student course enrollments")


@blp.route("/")
class EnrollmentList(MethodView):
    @blp.response(200, EnrollmentSchema(many=True))
    @roles_required("admin", "faculty")
    def get(self):
        """List enrollments."""
        return Enrollment.query.order_by(Enrollment.id.desc()).all()

    @blp.arguments(EnrollmentSchema, location="json")
    @blp.response(201, EnrollmentSchema)
    @roles_required("admin")
    def post(self, args):
        """Enroll a student to a course (admin only)."""
        student = Student.query.get(args["student_id"]) or abort(404, description="Student not found")
        course = Course.query.get(args["course_id"]) or abort(404, description="Course not found")
        existing = Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first()
        if existing:
            abort(400, description="Student already enrolled in course")
        enr = Enrollment(student_id=student.id, course_id=course.id)
        db.session.add(enr)
        db.session.commit()
        return enr


@blp.route("/<int:enrollment_id>")
class EnrollmentDetail(MethodView):
    @blp.response(200, EnrollmentSchema)
    @roles_required("admin", "faculty")
    def get(self, enrollment_id: int):
        """Get an enrollment."""
        return Enrollment.query.get_or_404(enrollment_id)

    @roles_required("admin")
    def delete(self, enrollment_id: int):
        """Remove an enrollment."""
        enr = Enrollment.query.get_or_404(enrollment_id)
        db.session.delete(enr)
        db.session.commit()
        return {"message": "Deleted"}
