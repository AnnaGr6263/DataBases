from db.connect_db import connect_to_db
from auth.encryption import hash_password
import bcrypt
import logging

def authenticate_user(username, password, user_type='user'):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            if user_type == 'user':
                cursor.execute("SELECT username, hashed_password FROM users WHERE username = %s", (username,))
            elif user_type == 'admin':
                cursor.execute("SELECT username, hashed_password FROM admins WHERE username = %s", (username,))
            elif user_type == 'artist':
                cursor.execute("SELECT name, hashed_password FROM artists WHERE name = %s", (username,))
            else:
                return False

            result = cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                logging.info("Password match")
                return True
            else:
                logging.info("Password does not match")
                return False
        except Exception as e:
            logging.error(f"Error authenticating user: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
