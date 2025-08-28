from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..extensions import db
from ..models import Attendance, Student, Course
from ..schemas import AttendanceSchema
from ..auth import roles_required

blp = Blueprint("Attendance", "attendance", url_prefix="/attendance", description="Attendance tracking")


@blp.route("/")
class AttendanceList(MethodView):
    @blp.response(200, AttendanceSchema(many=True))
    @roles_required("admin", "faculty")
    def get(self):
        """List attendance records."""
        return Attendance.query.order_by(Attendance.id.desc()).all()

    @blp.arguments(AttendanceSchema, location="json")
    @blp.response(201, AttendanceSchema)
    @roles_required("admin", "faculty")
    def post(self, args):
        """Mark attendance for a student in a course on a date."""
        _ = Student.query.get(args["student_id"]) or abort(404, description="Student not found")
        _ = Course.query.get(args["course_id"]) or abort(404, description="Course not found")
        # Ensure date is a date object (schema converts)
        existing = Attendance.query.filter_by(
            course_id=args["course_id"], student_id=args["student_id"], date=args["date"]
        ).first()
        if existing:
            abort(400, description="Attendance already recorded for this date")
        rec = Attendance(
            course_id=args["course_id"],
            student_id=args["student_id"],
            date=args["date"],
            status=args["status"],
        )
        db.session.add(rec)
        db.session.commit()
        return rec


@blp.route("/<int:attendance_id>")
class AttendanceDetail(MethodView):
    @blp.response(200, AttendanceSchema)
    @roles_required("admin", "faculty")
    def get(self, attendance_id: int):
        """Get attendance record."""
        return Attendance.query.get_or_404(attendance_id)

    @blp.arguments(AttendanceSchema, location="json")
    @blp.response(200, AttendanceSchema)
    @roles_required("admin", "faculty")
    def put(self, args, attendance_id: int):
        """Update attendance status."""
        rec = Attendance.query.get_or_404(attendance_id)
        for k in ["status", "date", "course_id", "student_id"]:
            if k in args:
                setattr(rec, k, args[k])
        db.session.commit()
        return rec

    @roles_required("admin", "faculty")
    def delete(self, attendance_id: int):
        """Delete attendance record."""
        rec = Attendance.query.get_or_404(attendance_id)
        db.session.delete(rec)
        db.session.commit()
        return {"message": "Deleted"}
