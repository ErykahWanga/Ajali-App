import sqlite3
import os

db_path = "/home/erykah/Ajali-Reporter/backend/instance/ajali.db"
print("🔍 Testing database access...")
print("📄 DB Path:", db_path)

# Check if directory exists and is writable
print("📁 DB Folder:", os.path.dirname(db_path))
print("✅ Folder exists:", os.path.exists(os.path.dirname(db_path)))
print("✅ Folder is writable:", os.access(os.path.dirname(db_path), os.W_OK))

try:
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test (name) VALUES (?)", ("test",))
    conn.commit()
    conn.close()
    print("🎉 SUCCESS: SQLite can read and write to the database!")
except Exception as e:
    print("❌ SQLite error:", e)
