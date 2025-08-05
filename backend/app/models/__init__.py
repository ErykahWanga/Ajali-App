from app.config import db
from app.models.User import User
from app.models.Incident import Incident

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.Comment import Comment
from flask import Blueprint
incidents_bp = Blueprint('incidents', __name__)
@incidents_bp.route('/<int:id>/comments', methods=['GET'])
def get_comments(id):
    comments = Comment.query.filter_by(incident_id=id).all()
    return jsonify([{
        'id': c.id,
        'text': c.text,
        'user': c.user.username,
        'created_at': c.created_at.isoformat()
    } for c in comments])

@incidents_bp.route('/<int:id>/comments', methods=['POST'])
@jwt_required()
def add_comment(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'message': 'Comment cannot be empty'}), 400

    comment = Comment(
        text=text,
        user_id=user_id,
        incident_id=id
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'id': comment.id,
        'text': comment.text,
        'user': user.username,
        'created_at': comment.created_at.isoformat()
    }), 201