import sqlite3
from datetime import datetime

# Connect to SQLite database (this creates example.db if it doesn't exist)
conn = sqlite3.connect("alx-airbnb-database.db")
cursor = conn.cursor()

# Create a table named 'users' with the correct schema
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number TEXT,
    role TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

# Insert some sample data
cursor.executemany("""
INSERT OR REPLACE INTO users (user_id, first_name, last_name, email, password_hash, phone_number, role, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('b8f2d6d5-1e25-44d0-a881-5b20e05c6121', 'Linda', 'Musyei', 'linds.host@example.com', 'hashed_pw1', '+254712345678', 'host', datetime.utcnow().isoformat()),
    ('c3eeb74b-7dc9-47b8-b8c6-fcc4fa8933cd', 'James', 'Kembo', 'james.guest@example.com', 'hashed_pw2', '+254700987654', 'guest', datetime.utcnow().isoformat()),
    ('d1a5cfe1-9e55-4c2f-92f3-74bd87ed014e', 'Derick', 'Avungashi', 'derick.admin@example.com', 'hashed_pw3', "", 'admin', datetime.utcnow().isoformat()),
    ('e34b7112-91e4-4adf-b812-0bb4ef762223', 'Abraham', 'Eve', 'eve.host@example.com', 'hashed_pw4', '+254713333333', 'host', datetime.utcnow().isoformat()),
    ('f92374d1-d0f1-4e6a-9b4f-f9e2f6f6de22', 'Emily', 'Mutiso', 'emily.guest@example.com', 'hashed_pw5', "", 'guest', datetime.utcnow().isoformat())
])

# Commit and close
conn.commit()
conn.close()

print("Database and table created with sample data.")
