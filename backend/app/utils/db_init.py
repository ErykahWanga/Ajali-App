# app/utils/db_init.py
from app import db
from app.models import User, Incident
from werkzeug.security import generate_password_hash
import os


def seed_data():
    # Avoid re-seeding if already exists
    if User.query.filter_by(username='admin').first():
        return

    print("Seeding default data...")

    # Create admin user
    admin = User(
        username='admin',
        email='admin@ajali.co.ke',
        is_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)

    # Create regular user
    user1 = User(
        username='james',
        email='james@kenya.co.ke'
    )
    user1.set_password('password')
    db.session.add(user1)

    # Commit users first to get their IDs
    db.session.commit()

    # Create mock incidents
    incidents = [
        Incident(
            title="Bus Crash on Thika Superhighway",
            description="Head-on collision between two matatus near Garden City. 3 injured.",
            latitude=-1.1942,
            longitude=36.8842,
            image_filename="bus_crash.jpg",
            user_id=admin.id
        ),
        Incident(
            title="Fire at Eastleigh Market",
            description="Electrical fire broke out in the electronics section. Firefighters responded.",
            latitude=-1.2738,
            longitude=36.8223,
            image_filename="fire.jpg",
            user_id=user1.id
        )
    ]

    for incident in incidents:
        # Create dummy image file if it doesn't exist
        image_path = f"instance/uploads/{incident.image_filename}"
        if not os.path.exists(image_path):
            with open(image_path, 'w') as f:
                f.write("\n")  # empty placeholder
        db.session.add(incident)

    db.session.commit()
    print("✅ Default data seeded: admin, user, and 2 incidents.")