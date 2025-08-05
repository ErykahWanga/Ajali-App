from flask import Blueprint, request, jsonify, send_from_directory, current_app
from app.config import db
from app.models import Incident, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.upload import allowed_file
import os
import time

incidents_bp = Blueprint('incidents', __name__)

@incidents_bp.route('', methods=['GET'])
def get_incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return jsonify([inc.to_dict() for inc in incidents])

@incidents_bp.route('/<int:id>', methods=['GET'])
def get_incident(id):
    incident = Incident.query.get_or_404(id)
    return jsonify(incident.to_dict())

@incidents_bp.route('', methods=['POST'])
@jwt_required()

@property
def likes_count(self):
    return Like.query.filter_by(incident_id=self.id).count()

def toggle_like(id):
    user_id = get_jwt_identity()
    incident = Incident.query.get_or_404(id)
    like = Like.query.filter_by(user_id=user_id, incident_id=id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'liked': False, 'likes': incident.likes_count}), 200
    else:
        new_like = Like(user_id=user_id, incident_id=id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'liked': True, 'likes': incident.likes_count}), 200

def create_incident():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not request.form.get('title') or not request.form.get('description'):
        return jsonify({'message': 'Title and description are required'}), 400

    try:
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
    except (ValueError, KeyError):
        return jsonify({'message': 'Valid latitude and longitude required'}), 400

    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename, current_app):
            filename = secure_filename(f"inc_{user_id}_{int(time.time())}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_filename = filename

    # ✅ Save incident with user_id
    incident = Incident(
        title=request.form['title'],
        description=request.form['description'],
        latitude=latitude,
        longitude=longitude,
        image_filename=image_filename,
        user_id=user_id  # ← Critical: link to user
    )
    db.session.add(incident)
    db.session.commit()

    return jsonify(incident.to_dict()), 201

@incidents_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()

def add_comment(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()

    if not data.get('content'):
        return jsonify({'message': 'Comment cannot be empty'}), 400

    comment = Comment(
        content=data['content'],
        user_id=user_id,
        incident_id=id
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'author': user.username,
        'created_at': comment.created_at.isoformat()
    }), 201
def delete_incident(id):
    user_id = get_jwt_identity()
    incident.likes = (incident.likes or 0) + 1
    incident = Incident.query.get_or_404(id)

    user = User.query.get(user_id)
    if not user.is_admin and incident.user_id != user_id:
        return jsonify({'message': 'Permission denied'}), 403

    if incident.image_filename:
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], incident.image_filename)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(incident)
    db.session.commit()
    return jsonify({'message': 'Incident deleted'}), 200