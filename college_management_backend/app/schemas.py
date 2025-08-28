from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    total = fields.Int()
    total_pages = fields.Int()
    first_page = fields.Int()
    last_page = fields.Int()
    page = fields.Int()
    previous_page = fields.Int(allow_none=True)
    next_page = fields.Int(allow_none=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    role = fields.Str(validate=validate.OneOf(["admin", "faculty", "student"]))
    is_active = fields.Bool()


class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(required=True, validate=validate.OneOf(["admin", "faculty", "student"]))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class TokenSchema(Schema):
    access_token = fields.Str(required=True)
    token_type = fields.Str(required=True, default="bearer")


class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    roll_number = fields.Str(required=True)
    department = fields.Str(required=True)
    year = fields.Int(required=True)


class FacultySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    employee_id = fields.Str(required=True)
    department = fields.Str(required=True)
    designation = fields.Str(allow_none=True)


class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
    title = fields.Str(required=True)
    credits = fields.Int(required=True)
    faculty_id = fields.Int(allow_none=True)


class EnrollmentSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)


class AttendanceSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    date = fields.Date(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["present", "absent"]))


class GradeSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    grade = fields.Str(required=True)
