import os
from werkzeug.utils import secure_filename

def allowed_file(filename, app):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return '.' in filename and ext in app.config['ALLOWED_EXTENSIONS']