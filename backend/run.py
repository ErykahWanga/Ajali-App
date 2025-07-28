from app import create_app, db
from app.models import User, Incident
import random
import os
from datetime import datetime, timedelta
from PIL import Image
import io
import base64

app = create_app()

def create_sample_images():
    """Create sample images for incidents"""
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # Sample base64 encoded images (you can replace these with your own)
    sample_images = [
        # Car accident image
        "data:image/jpeg;base64,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",
        # Matatu image
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
        # Truck image
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mO0ZGD4DwAEiwGOU65syQAAAABJRU5ErkJggg==",
        # Motorcycle image
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPj/HwADggGOT2C23AAAAABJRU5ErkJggg==",
        # Bus image
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYGD4DwAEiwGOU65syQAAAABJRU5ErkJggg=="
    ]
    
    image_filenames = []
    for i, img_data in enumerate(sample_images):
        filename = f"sample_incident_{i+1}.png"
        filepath = os.path.join(upload_folder, filename)
        
        # Create a simple colored image for demo
        img = Image.new('RGB', (400, 300), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        img.save(filepath, 'PNG')
        image_filenames.append(filename)
    
    return image_filenames

def create_sample_data():
    with app.app_context():
        # Check if we already have incidents
        if Incident.query.count() > 5:
            return
            
        # Create sample images
        image_filenames = create_sample_images()
        
        # Create sample incidents with images
        sample_incidents = [
            {
                "title": "Major Car Accident on Mombasa Road",
                "description": "Multi-vehicle collision near Junction Mall. Emergency services on scene.",
                "latitude": -1.3032,
                "longitude": 36.8295,
                "image_filename": image_filenames[0] if len(image_filenames) > 0 else None
            },
            {
                "title": "Matatu Overturns in Ngong",
                "description": "14-seater matatu overturned near Ngong Hills. Several injuries reported.",
                "latitude": -1.3573,
                "longitude": 36.6598,
                "image_filename": image_filenames[1] if len(image_filenames) > 1 else None
            },
            {
                "title": "Truck Spills Cargo on Thika Superhighway",
                "description": "Lorry carrying construction materials loses cargo. Causing major traffic delays.",
                "latitude": -1.1518,
                "longitude": 37.0073,
                "image_filename": image_filenames[2] if len(image_filenames) > 2 else None
            },
            {
                "title": "Motorcycle Accident near Westlands",
                "description": "Bike rider collided with taxi. Rider sustained minor injuries.",
                "latitude": -1.2642,
                "longitude": 36.8034,
                "image_filename": image_filenames[3] if len(image_filenames) > 3 else None
            },
            {
                "title": "Bus Breakdown on Langata Road",
                "description": "Commuter bus broke down during rush hour. Passengers stranded.",
                "latitude": -1.3129,
                "longitude": 36.7892,
                "image_filename": image_filenames[4] if len(image_filenames) > 4 else None
            },
            {
                "title": "Lorry Fire on Eastern Bypass",
                "description": "Trailer truck caught fire near Embakasi. Fire department responding.",
                "latitude": -1.3230,
                "longitude": 36.9178,
                "image_filename": image_filenames[0] if len(image_filenames) > 0 else None
            },
            {
                "title": "Tuk-tuk Collision in CBD",
                "description": "Two tuk-tuks collided at Tom Mboya Street junction during peak hours.",
                "latitude": -1.2833,
                "longitude": 36.8167,
                "image_filename": image_filenames[1] if len(image_filenames) > 1 else None
            },
            {
                "title": "Fuel Spillage on Waiyaki Way",
                "description": "Tanker truck leaking fuel near Karura Forest. Road partially closed.",
                "latitude": -1.2544,
                "longitude": 36.7789,
                "image_filename": image_filenames[2] if len(image_filenames) > 2 else None
            },
            {
                "title": "Pedestrian Hit near University Way",
                "description": "Student struck by matatu near UoN grounds. Ambulance on scene.",
                "latitude": -1.2630,
                "longitude": 36.8145,
                "image_filename": image_filenames[3] if len(image_filenames) > 3 else None
            },
            {
                "title": "Construction Vehicle Accident in Karen",
                "description": "Excavator collided with private vehicle. No serious injuries reported.",
                "latitude": -1.3584,
                "longitude": 36.7021,
                "image_filename": image_filenames[4] if len(image_filenames) > 4 else None
            },
            {
                "title": "Bicycle vs Car near Parklands",
                "description": "Cyclist injured after collision with private car. Traffic police investigating.",
                "latitude": -1.2585,
                "longitude": 36.8038,
                "image_filename": image_filenames[0] if len(image_filenames) > 0 else None
            },
            {
                "title": "Matatu Fire in Githurai",
                "description": "14-seater caught fire near Githurai 44. Passengers evacuated safely.",
                "latitude": -1.2284,
                "longitude": 36.8872,
                "image_filename": image_filenames[1] if len(image_filenames) > 1 else None
            },
            {
                "title": "Lorry Overturns on Nakuru Highway",
                "description": "Truck carrying goods overturned near Mai Mahiu. Road blocked.",
                "latitude": -1.0884,
                "longitude": 36.2214,
                "image_filename": image_filenames[2] if len(image_filenames) > 2 else None
            },
            {
                "title": "Motorcycle vs Pedestrian in Donholm",
                "description": "Rider hits pedestrian crossing illegally. Both parties injured.",
                "latitude": -1.3023,
                "longitude": 36.8967,
                "image_filename": image_filenames[3] if len(image_filenames) > 3 else None
            },
            {
                "title": "Taxi Collision in Mombasa CBD",
                "description": "Two taxis collide at Likoni Ferry terminus. Minor injuries reported.",
                "latitude": -4.0435,
                "longitude": 39.6682,
                "image_filename": image_filenames[4] if len(image_filenames) > 4 else None
            }
        ]
        
        # Create a default admin user if none exists
        if not User.query.filter_by(email="admin@ajali.reporter").first():
            admin = User(
                username="admin",
                email="admin@ajali.reporter",
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
        
        # Get the admin user
        admin_user = User.query.filter_by(email="admin@ajali.reporter").first()
        
        # Add sample incidents to database
        for i, incident_data in enumerate(sample_incidents):
            # Add some time variation to created_at
            created_at = datetime.utcnow() - timedelta(hours=random.randint(1, 72))
            
            incident = Incident(
                title=incident_data["title"],
                description=incident_data["description"],
                latitude=incident_data["latitude"],
                longitude=incident_data["longitude"],
                image_filename=incident_data["image_filename"],
                reporter_id=admin_user.id,
                created_at=created_at,
                updated_at=created_at
            )
            db.session.add(incident)
        
        db.session.commit()
        print(f"Added {len(sample_incidents)} sample incidents with images to database")

# Create tables and sample data
with app.app_context():
    db.create_all()
    create_sample_data()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)