import os


class Config:
    """Base configuration loaded from environment variables."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")  # For session/JWT signing only in dev
    # DB connection via env vars from the database container (do not assume actual values)
    MYSQL_URL = os.getenv("MYSQL_URL", "")
    MYSQL_USER = os.getenv("MYSQL_USER", "")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "")

    # SQLAlchemy DB URI; if MySQL* variables exist, compose a URI, else fallback to SQLite file for local dev
    if all([MYSQL_URL, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT]):
        # MYSQL_URL expected like hostname or full host, use standard pymysql driver
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DB}"
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "sqlite:///college.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT-like settings (we'll implement a lightweight token approach)
    ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES", "60"))

    # CORS origins (comma separated), default allow all for development
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
