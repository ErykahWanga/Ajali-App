import os
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

class Config:
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-change-in-production"
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 1 day in seconds

    # Database configuration with fallback
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        # Fallback to SQLite in instance folder
        instance_path = Path(__file__).parent.parent / "instance"
        instance_path.mkdir(exist_ok=True)
        DATABASE_URL = f"sqlite:///{instance_path}/app.db"
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER") or "instance/uploads"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy()