from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Incident, User
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import send_from_directory

bp = Blueprint('incidents', __name__)

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
            from PIL import Image
            img = Image.open(filepath)
            img.thumbnail((800, 800))  # Resize to max 800x800
            img.save(filepath, optimize=True, quality=85)
        except Exception:
            pass  # If optimization fails, keep original
        
        return filename
    return None

@bp.route('', methods=['GET'], strict_slashes=False)
def get_incidents():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        incidents = Incident.query.order_by(Incident.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
        
        return jsonify([incident.to_dict() for incident in incidents.items]), 200
    except Exception as e:
        current_app.logger.error(f"Get incidents error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_incidents():
    try:
        current_user_id = get_jwt_identity()
        incidents = Incident.query.filter_by(reporter_id=current_user_id)\
            .order_by(Incident.created_at.desc()).all()
        
        return jsonify([incident.to_dict() for incident in incidents]), 200
    except Exception as e:
        current_app.logger.error(f"Get my incidents error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/<int:id>', methods=['GET'])
def get_incident(id):
    try:
        incident = Incident.query.get_or_404(id)
        return jsonify(incident.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Get incident error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_incident():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        # Validate required fields
        required_fields = ['title', 'description', 'latitude', 'longitude']
        for field in required_fields:
            if not request.form.get(field):
                return jsonify({'message': f'{field} is required'}), 400
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_filename = save_image(image_file, current_app.config['UPLOAD_FOLDER'])
        
        # Create incident
        incident = Incident(
            title=request.form['title'],
            description=request.form['description'],
            latitude=float(request.form['latitude']),
            longitude=float(request.form['longitude']),
            image_filename=image_filename,
            reporter_id=user.id
        )
        
        db.session.add(incident)
        db.session.commit()
        
        return jsonify(incident.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create incident error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        current_app.logger.error(f"Serve upload error: {str(e)}")
        return jsonify({'message': 'File not found'}), 404

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_incident(id):
    try:
        current_user_id = get_jwt_identity()
        incident = Incident.query.get_or_404(id)
        
        # Check if user is authorized to update
        if incident.reporter_id != current_user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Update fields
        if 'title' in request.form:
            incident.title = request.form['title']
        if 'description' in request.form:
            incident.description = request.form['description']
        if 'latitude' in request.form:
            incident.latitude = float(request.form['latitude'])
        if 'longitude' in request.form:
            incident.longitude = float(request.form['longitude'])
        
        # Handle image update
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Delete old image if exists
                if incident.image_filename:
                    old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], incident.image_filename)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                
                # Save new image
                incident.image_filename = save_image(image_file, current_app.config['UPLOAD_FOLDER'])
        
        db.session.commit()
        return jsonify(incident.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update incident error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_incident(id):
    try:
        current_user_id = get_jwt_identity()
        incident = Incident.query.get_or_404(id)
        
        # Check if user is authorized to delete
        if incident.reporter_id != current_user_id and not User.query.get(current_user_id).is_admin:
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Delete image file if exists
        if incident.image_filename:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], incident.image_filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        db.session.delete(incident)
        db.session.commit()
        
        return jsonify({'message': 'Incident deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete incident error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500