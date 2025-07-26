from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Incident, User

bp = Blueprint('admin', __name__)

@bp.route('/incidents', methods=['GET'])
@jwt_required()
def get_all_incidents():
    """Admin: Get all incidents"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({'message': 'Admin access required'}), 403
    
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return jsonify([incident.to_dict() for incident in incidents]), 200

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Admin: Get all users"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({'message': 'Admin access required'}), 403
    
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@bp.route('/incidents/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_incident(id):
    """Admin: Delete an incident"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({'message': 'Admin access required'}), 403
    
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    
    return jsonify({'message': 'Incident deleted'}), 200