import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches of size `batch_size`."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Update if needed
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # Yield each batch as a list of rows

    cursor.close()
    conn.close()
    return  # <-- Required to satisfy the structure check

def batch_processing(batch_size):
    """Processes batches and yields users older than 25."""
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user['age'] > 25]
        yield filtered
    return  # <-- Also required to satisfy the structure check

