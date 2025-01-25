import mariadb
import logging
import os

def connect_to_db():
    try:
        connection = mariadb.connect(
            host=os.getenv("DB_HOST", "localhost"),        # Nazwa hosta, np. 'localhost' lub IP
            user=os.getenv("DB_USER", "root"),  # Nazwa użytkownika
            password=os.getenv("DB_PASSWORD", ""),  # Hasło użytkownika
            database=os.getenv("DB_NAME", "spotifydb")    # Nazwa bazy danych
        )
        if connection:
            logging.debug("Połączono z bazą danych")
            return connection
    except mariadb.Error as e:
        logging.error(f"Nie udało się połączyć z bazą: {e}")
        return None
