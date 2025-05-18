import mysql.connector
import csv
import uuid

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''  # Put your MySQL root password here

CSV_FILE = 'user_data.csv'

def connect_db():
    """Connect to MySQL server (no specific database)."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database="ALX_prodev"
    )

def create_table(connection):
    """Create user_data table with specified schema."""
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX idx_user_id(user_id)
    )
    """)
    cursor.close()

def insert_data(connection, data):
    """
    Insert data into user_data table.
    'data' is expected as a list of dicts with keys: user_id, name, email, age
    Skip if user_id already exists.
    """
    cursor = connection.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    for row in data:
        cursor.execute(insert_query, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()

def read_csv(file_path):
    """Read CSV and yield rows as dicts."""
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Ensure user_id is a valid UUID string, or generate one if missing
            user_id = row.get('user_id') or str(uuid.uuid4())
            yield {
                'user_id': user_id,
                'name': row['name'],
                'email': row['email'],
                'age': float(row['age']),
            }

def stream_rows(connection):
    """Generator that fetches rows one by one from user_data table."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()

def main():
    # Connect to MySQL server (no DB)
    conn = connect_db()
    create_database(conn)
    conn.close()

    # Connect to ALX_prodev database
    conn = connect_to_prodev()
    create_table(conn)

    # Read data from CSV and insert into table
    data = list(read_csv(CSV_FILE))
    insert_data(conn, data)

    # Example: stream rows and print them one by one
    print("Streaming rows from user_data:")
    for user_row in stream_rows(conn):
        print(user_row)

    conn.close()

if __name__ == "__main__":
    main()
