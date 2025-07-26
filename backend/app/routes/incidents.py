from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Incident, User
from app.utils import save_image, allowed_file

bp = Blueprint('incidents', __name__)

@bp.route('/incidents', methods=['GET'])
def get_incidents():
    """Get all incidents (public)"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    
    incidents = Incident.query.order_by(Incident.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return jsonify([incident.to_dict() for incident in incidents.items]), 200

@bp.route('/incidents', methods=['POST'])
@jwt_required()
def create_incident():
    """Create a new incident"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Validate input
    required_fields = ['title', 'description', 'latitude', 'longitude']
    for field in required_fields:
        if not request.form.get(field):
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Handle image upload
    image_url = None
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            image_url = save_image(image_file)
    
    # Create incident
    incident = Incident(
        title=request.form['title'],
        description=request.form['description'],
        latitude=float(request.form['latitude']),
        longitude=float(request.form['longitude']),
        image_url=image_url,
        user_id=user.id
    )
    
    db.session.add(incident)
    db.session.commit()
    
    return jsonify(incident.to_dict()), 201

@bp.route('/incidents/<int:id>', methods=['GET'])
def get_incident(id):
    """Get a specific incident"""
    incident = Incident.query.get_or_404(id)
    return jsonify(incident.to_dict()), 200

@bp.route('/user/incidents', methods=['GET'])
@jwt_required()
def get_user_incidents():
    """Get incidents for the current user"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    incidents = Incident.query.filter_by(user_id=user.id).order_by(Incident.created_at.desc()).all()
    return jsonify([incident.to_dict() for incident in incidents]), 200