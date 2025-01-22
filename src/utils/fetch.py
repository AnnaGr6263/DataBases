from src.utils.connect_db import connect_to_db

def fetch_users():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
