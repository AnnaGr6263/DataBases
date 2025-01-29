import mariadb
import logging
import os

def connect_to_db(role="default"):
    try:
        if role == "readonly":
            user = os.getenv("DB_USER_READONLY", "readonly_user")
            password = os.getenv("DB_PASSWORD_READONLY", "readonly_password")
        elif role == "artist":
            user = os.getenv("DB_USER_ARTIST", "artist_user")
            password = os.getenv("DB_PASSWORD_ARTIST", "artist_password")
        else:
            user = os.getenv("DB_USER", "root")
            password = os.getenv("DB_PASSWORD", "")
        
        connection = mariadb.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=user,
            password=password,
            database=os.getenv("DB_NAME", "spotifydb")
        )
        if connection:
            logging.debug("Połączono z bazą danych")
            return connection
    except mariadb.Error as e:
        logging.error(f"Nie udało się połączyć z bazą: {e}")
        return None
