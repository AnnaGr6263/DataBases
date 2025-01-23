from src.db.fetch import fetch_users
from src.auth.encryption import hash_password
import bcrypt

def authenticate_user(username, password):
    users = fetch_users()
    for user in users:
        if user['username'] == username and bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
            return True
    return False
