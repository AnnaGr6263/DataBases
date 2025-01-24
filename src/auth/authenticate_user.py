from db.fetch import fetch_users, fetch_admins
from auth.encryption import hash_password
import bcrypt
import logging

def authenticate_user(username, password, user_type='user'):
    if user_type == 'admin':
        users = fetch_admins()
    else:
        users = fetch_users()
    
    logging.info(f"Fetched {user_type}s: {users}")
    for user in users:
        if user['username'] == username:
            logging.info(f"Found {user_type}: {user}")
            if bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
                logging.info("Password match")
                return True
            else:
                logging.info("Password does not match")
    return False
