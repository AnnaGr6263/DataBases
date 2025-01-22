from src.utils.connect_db import connect_to_db

def add_user(username, email, hashed_password):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        connection.commit()
        cursor.close()
        connection.close()
