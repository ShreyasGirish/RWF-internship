import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

# Create database connection
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create attendance table
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    image_path TEXT
)
''')

# Create sample data
cursor.execute("INSERT OR IGNORE INTO attendance (name, date, time, image_path) VALUES ('John Doe', '2024-04-21', '10:30', '/captures/john/capture1.jpg')")
cursor.execute("INSERT OR IGNORE INTO attendance (name, date, time, image_path) VALUES ('Jane Smith', '2024-04-21', '11:15', '/captures/jane/capture2.jpg')")

conn.commit()
conn.close()

print(f"✅ Database '{DB_PATH}' created with schema and sample data!")
print("Tables: attendance")

