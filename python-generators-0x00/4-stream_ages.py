## Implement a generator stream_user_ages() that yields user ages one by one.
import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one from the user_data table."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Add your MySQL root password if needed
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # fetch one column per row
        yield age

    cursor.close()
    conn.close()
    return
if __name__ == "__main__":
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age: {average:.2f}")
    else:
        print("No users found.")



import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Update if needed
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # ✅ Loop 1
        yield age

    cursor.close()
    conn.close()
    return

def calculate_average_age():
    """Calculates and prints the average age using the generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():  # ✅ Loop 2
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
