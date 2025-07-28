import os
from werkzeug.utils import secure_filename
from PIL import Image

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, upload_folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(datetime.utcnow().timestamp())}{ext}"
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Optimize image
        try:
            img = Image.open(filepath)
            img.thumbnail((800, 800))  # Resize to max 800x800
            img.save(filepath, optimize=True, quality=85)
        except Exception:
            pass  # If optimization fails, keep original
        
        return filename
    return None