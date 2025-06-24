import sqlite3

# Connect to the database
conn = sqlite3.connect("med_tracker.db")
cursor = conn.cursor()

# Create medications table (if not already)
cursor.execute("""
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug TEXT NOT NULL,
    dose_time TEXT NOT NULL,
    frequency TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# ✅ Step 1: Create the dose_logs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dose_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    med_id INTEGER NOT NULL,
    taken_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (med_id) REFERENCES medications(id)
)
""")

conn.commit()
conn.close()

print("✅ Database initialized and dose_logs table created.")
