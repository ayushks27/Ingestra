import sqlite3
import pandas as pd

DB_PATH = r"D:\projects\Ingestra\yelp.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create business table
c.execute("""
CREATE TABLE IF NOT EXISTS business (
    b_id TEXT PRIMARY KEY,
    name TEXT,
    postal_code TEXT
)
""")

# Load CSV
business_df = pd.read_csv("data/business_data.csv")

# 🔑 CRITICAL FIX: strip whitespace from column names
business_df.columns = business_df.columns.str.strip()

# Debug
print("Cleaned columns:", business_df.columns)

# Rename after cleaning
business_df.rename(
    columns={"business_id": "b_id"},
    inplace=True
)

# Select required columns
business_df = business_df[["b_id", "name", "postal_code"]]

# Load into DB
business_df.to_sql(
    "business",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()
conn.close()

print("✅ Database setup complete.")
