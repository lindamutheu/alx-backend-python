import mysql.connector

def paginate_users(page_size, offset):
    """Fetch a single page of users starting from the given offset."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Add your password if needed
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def lazy_paginate(page_size):
    """Generator that lazily loads each page of users using pagination."""
    offset = 0
    while True:  # ✅ Only one loop used
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
    return
