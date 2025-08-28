from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # roles: admin, faculty, student
    role = db.Column(db.String(50), nullable=False, default="student")
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    student_profile = db.relationship("Student", uselist=False, back_populates="user")
    faculty_profile = db.relationship("Faculty", uselist=False, back_populates="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Student(db.Model, TimestampMixin):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    roll_number = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="student_profile")
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")


class Faculty(db.Model, TimestampMixin):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    employee_id = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=True)

    user = db.relationship("User", back_populates="faculty_profile")
    courses = db.relationship("Course", back_populates="faculty")


class Course(db.Model, TimestampMixin):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=3)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=True)

    faculty = db.relationship("Faculty", back_populates="courses")
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="course", cascade="all, delete-orphan")
    grades = db.relationship("Grade", back_populates="course", cascade="all, delete-orphan")


class Enrollment(db.Model, TimestampMixin):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

    __table_args__ = (db.UniqueConstraint("student_id", "course_id", name="uq_student_course"),)


class Attendance(db.Model, TimestampMixin):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="present")  # present/absent

    course = db.relationship("Course", back_populates="attendance_records")
    student = db.relationship("Student")

    __table_args__ = (db.UniqueConstraint("course_id", "student_id", "date", name="uq_attendance_unique"),)


class Grade(db.Model, TimestampMixin):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    grade = db.Column(db.String(5), nullable=False)

    course = db.relationship("Course", back_populates="grades")
    student = db.relationship("Student")

    __table_args__ = (db.UniqueConstraint("course_id", "student_id", name="uq_grade_unique"),)
