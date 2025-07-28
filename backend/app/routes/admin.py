from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Incident, User
import os

bp = Blueprint('admin', __name__)

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        # Check if user is admin
        if not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get statistics
        total_incidents = Incident.query.count()
        total_users = User.query.count()
        recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
        
        return jsonify({
            'total_incidents': total_incidents,
            'total_users': total_users,
            'recent_incidents': [incident.to_dict() for incident in recent_incidents]
        }), 200
    except Exception as e:
        current_app.logger.error(f"Admin dashboard error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/incidents', methods=['GET'])
@jwt_required()
def get_all_incidents():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        # Check if user is admin
        if not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        incidents = Incident.query.order_by(Incident.created_at.desc()).all()
        return jsonify([incident.to_dict() for incident in incidents]), 200
    except Exception as e:
        current_app.logger.error(f"Get all incidents error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/incidents/<int:id>/approve', methods=['POST'])
@jwt_required()
def approve_incident(id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        # Check if user is admin
        if not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        incident = Incident.query.get_or_404(id)
        # In a real app, you might have an 'approved' field to set
        # For now, we'll just return success
        return jsonify({'message': 'Incident approved'}), 200
    except Exception as e:
        current_app.logger.error(f"Approve incident error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/incidents/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def admin_delete_incident(id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        # Check if user is admin
        if not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        incident = Incident.query.get_or_404(id)
        
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
        current_app.logger.error(f"Admin delete incident error: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500