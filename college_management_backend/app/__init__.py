from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .config import DevConfig
from .extensions import db

# Blueprints
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.users import blp as users_blp
from .routes.students import blp as students_blp
from .routes.faculty import blp as faculty_blp
from .routes.courses import blp as courses_blp
from .routes.enrollment import blp as enrollment_blp
from .routes.attendance import blp as attendance_blp
from .routes.grades import blp as grades_blp
from .routes.admin import blp as admin_blp


app = Flask(__name__)
app.url_map.strict_slashes = False

# Load config (Dev by default; production can set FLASK_ENV/override with env variables)
app.config.from_object(DevConfig)

# CORS
cors_origins = app.config.get("CORS_ORIGINS", "*")
CORS(app, resources={r"/*": {"origins": cors_origins}})

# OpenAPI / Swagger UI configuration
app.config["API_TITLE"] = "College Management API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Init extensions
api = Api(app)
db.init_app(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(auth_blp)
api.register_blueprint(users_blp)
api.register_blueprint(students_blp)
api.register_blueprint(faculty_blp)
api.register_blueprint(courses_blp)
api.register_blueprint(enrollment_blp)
api.register_blueprint(attendance_blp)
api.register_blueprint(grades_blp)
api.register_blueprint(admin_blp)

# Create tables automatically in dev mode if using SQLite (for demo)
with app.app_context():
    try:
        from sqlalchemy import text  # ensure SQLAlchemy available
        db.create_all()
    except Exception:
        # In production with managed migrations, ignore create_all failures
        pass
