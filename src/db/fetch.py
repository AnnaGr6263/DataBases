from src.db.connect_db import connect_to_db
import logging

def fetch_users():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT username, hashed_password FROM users")
            users = cursor.fetchall()
            logging.info(f"Fetched users from database: {users}")
            return [{"username": user[0], "hashed_password": user[1]} for user in users]
        except Exception as e:
            logging.error(f"Error fetching users: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    return []

def fetch_admins():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT username, hashed_password FROM admins")
            admins = cursor.fetchall()
            logging.info(f"Fetched admins from database: {admins}")
            return [{"username": admin[0], "hashed_password": admin[1]} for admin in admins]
        except Exception as e:
            logging.error(f"Error fetching admins: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    return []
