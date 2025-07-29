# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    # Load DATABASE_URL from .env
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL is not set! Check .env and python-dotenv.")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER") or "instance/uploads"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-change-in-production"
    JWT_ACCESS_TOKEN_EXPIRES = 86400