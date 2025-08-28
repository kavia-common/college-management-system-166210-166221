from flask_smorest import Blueprint
from flask.views import MethodView
from ..models import User, Student, Faculty, Course, Enrollment, Attendance, Grade
from ..auth import roles_required

blp = Blueprint("Admin", "admin", url_prefix="/admin", description="Admin panel utilities")


@blp.route("/stats")
class AdminStats(MethodView):
    @roles_required("admin")
    def get(self):
        """Basic dashboard statistics for admin."""
        return {
            "users": User.query.count(),
            "students": Student.query.count(),
            "faculty": Faculty.query.count(),
            "courses": Course.query.count(),
            "enrollments": Enrollment.query.count(),
            "attendance_records": Attendance.query.count(),
            "grades": Grade.query.count(),
        }
