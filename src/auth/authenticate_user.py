from src.db.fetch import fetch_users
from src.auth.encryption import hash_password

def authenticate_user(username, password):
    users = fetch_users()
    for user in users:
        if user['username'] == username and user['hashed_password'] == hash_password(password):
            return True
    return False
