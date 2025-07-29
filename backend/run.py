# run.py
from dotenv import load_dotenv  # ← Add this at the top
from app import create_app, db
from app.utils.db_init import seed_data
import os

# Load environment variables BEFORE importing create_app
load_dotenv()

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created!")
    except Exception as e:
        print("❌ Failed to create tables:", str(e))
        exit(1)

    seed_data()

if __name__ == '__main__':
    print("🌍 Ajali Reporter Backend running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
