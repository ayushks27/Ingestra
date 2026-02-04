import sqlite3
import pandas as pd

# Create demo database
conn = sqlite3.connect("yelp_demo.db")
cursor = conn.cursor()

# Create business table
cursor.execute("""
CREATE TABLE IF NOT EXISTS business (
    b_id TEXT PRIMARY KEY,
    name TEXT,
    postal_code TEXT
)
""")

# Create predicted_reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predicted_reviews (
    business_id TEXT,
    Review TEXT,
    Stars REAL,
    authenticity_label INTEGER
)
""")

# Insert demo business data
business_data = [
    ("b1", "Demo Cafe", "226021"),
    ("b2", "Sample Diner", "226021")
]

cursor.executemany(
    "INSERT OR REPLACE INTO business VALUES (?, ?, ?)",
    business_data
)

# Insert demo reviews
review_data = [
    ("b1", "Great food and friendly staff", 4.5, 1),
    ("b1", "Amazing experience overall", 5.0, 1),
    ("b2", "Average service", 3.0, 1),
    ("b2", "Not worth the price", 2.0, 0)
]

cursor.executemany(
    "INSERT INTO predicted_reviews VALUES (?, ?, ?, ?)",
    review_data
)

conn.commit()
conn.close()

print("Demo database created: yelp_demo.db")
