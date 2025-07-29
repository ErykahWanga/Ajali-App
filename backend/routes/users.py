from flask import Blueprint, jsonify
from app.models import User, Incident
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/<int:user_id>/incidents', methods=['GET'])
@jwt_required()
def get_user_incidents(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    # Allow access if user is viewing own reports or is admin
    current_user = User.query.get(current_user_id)
    if user_id != current_user_id and not current_user.is_admin:
        return jsonify({'message': 'Forbidden'}), 403

    incidents = Incident.query.filter_by(user_id=user_id).order_by(Incident.created_at.desc()).all()
    return jsonify([inc.to_dict() for inc in incidents])