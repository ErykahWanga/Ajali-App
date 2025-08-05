# run.py
from dotenv import load_dotenv  # ← Add this at the top
load_dotenv()

import os

# Load environment variables BEFORE importing create_app
from app import create_app

app = create_app()

with app.app_context():
    try:
        from app.config import db
        db.create_all()
        print("✅ Database tables created!")
    except Exception as e:
        print("❌ Failed to create tables:", str(e))
        exit(1)

    from app.utils.db_init import seed_data
    seed_data()

if __name__ == '__main__':
    print("🌍 Ajali Reporter Backend running on http://localhost:5500")
    app.run(host='0.0.0.0', port=5500, debug=False)
