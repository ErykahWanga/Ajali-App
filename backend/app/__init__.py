# app/__init__.py
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from app.config import Config
    app.config.from_object(Config)

    # 👇 Disable URI mode
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'uri': False}
    }

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.incidents import incidents_bp
    from app.routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(incidents_bp, url_prefix='/api/incidents')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    # Serve uploaded files
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
