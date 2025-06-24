import sqlite3

conn = sqlite3.connect("med_tracker.db")
cursor = conn.cursor()

sample_meds = [
    ("Warfarin", "5mg", "08:00,20:00", 60),
    ("Metformin", "500mg", "09:00,21:00", 90),
    ("Amlodipine", "10mg", "07:30", 30)
]

for med in sample_meds:
    cursor.execute("""
    INSERT INTO medications (name, dose, schedule, quantity)
    VALUES (?, ?, ?, ?)
    """, med)

conn.commit()
conn.close()

print("✅ Sample medications added.")
