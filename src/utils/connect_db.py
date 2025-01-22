import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",        # Nazwa hosta, np. 'localhost' lub IP
            user="twoja_nazwa_uzytkownika",  # Nazwa użytkownika
            password="twoje_haslo",  # Hasło użytkownika
            database="twoja_baza"    # Nazwa bazy danych
        )
        if connection.is_connected():
            print("Połączono z bazą danych")
            return connection
    except Exception as e:
        print(f"Nie udało się połączyć z bazą: {e}")
        return None
