import os
from dotenv import load_dotenv

# Try to load .env
load_dotenv()

print("🔍 Current directory:", os.getcwd())
print("📄 .env file exists:", os.path.exists('.env'))

print("\n🔐 Environment variables:")
print("  DATABASE_URL =", os.environ.get("DATABASE_URL"))
print("  FLASK_APP =", os.environ.get("FLASK_APP"))

if os.environ.get("DATABASE_URL"):
    print("\n✅ Success: .env is loaded!")
else:
    print("\n❌ Failed: DATABASE_URL is missing. python-dotenv may not be working.")
