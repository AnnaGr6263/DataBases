from db.connect_db import connect_to_db
import logging
from auth.encryption import hash_password  # Add this import

def create_indexes():
    # Tworzy indeksy w bazie dla szybszego wyszukiwania.
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_songs_title ON songs (title);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_playlists_name ON playlists (name);")
            connection.commit()
            logging.info("Indeksy zostały dodane!")
        except Exception as e:
            logging.error(f"Błąd tworzenia indeksów: {e}")
        finally:
            cursor.close()
            connection.close()

def create_like_count_functions():
    # Tworzy funkcje SQL do liczenia polubień dla utworów, albumów i artystów.
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            CREATE FUNCTION IF NOT EXISTS count_song_likes(song_id INT) RETURNS INT
            BEGIN
                DECLARE like_count INT;
                SELECT COUNT(*) INTO like_count FROM song_likes WHERE id_song = song_id;
                RETURN like_count;
            END;
            """)

            cursor.execute("""
            CREATE FUNCTION IF NOT EXISTS count_album_likes(album_id INT) RETURNS INT
            BEGIN
                DECLARE like_count INT;
                SELECT COUNT(*) INTO like_count FROM album_likes WHERE id_album = album_id;
                RETURN like_count;
            END;
            """)

            cursor.execute("""
            CREATE FUNCTION IF NOT EXISTS count_artist_likes(artist_id INT) RETURNS INT
            BEGIN
                DECLARE like_count INT;
                SELECT COUNT(*) INTO like_count FROM artist_likes WHERE id_artist = artist_id;
                RETURN like_count;
            END;
            """)

            connection.commit()
            logging.info("Funkcje count_likes zostały dodane!")
        except Exception as e:
            logging.error(f"Błąd tworzenia funkcji: {e}")
        finally:
            cursor.close()
            connection.close()

def setup_database():
    # Sprawdza i konfiguruje bazę danych przed startem aplikacji.
    logging.info("🔄 Sprawdzanie konfiguracji bazy danych...")
    create_indexes()
    create_like_count_functions()
    
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Check if the first admin exists
        cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
        admin_exists = cursor.fetchone()[0]
        logging.info(f"Admin exists: {admin_exists}")

        if admin_exists == 0:
            # Insert the first admin
            first_admin_username = "admin"
            first_admin_email = "admin@example.com"
            first_admin_password = "adminpassword"
            hashed_password = hash_password(first_admin_password)
            logging.info(f"Creating admin user with username: {first_admin_username}, email: {first_admin_email}")

            cursor.execute("""
                INSERT INTO admins (username, email, hashed_password)
                VALUES (%s, %s, %s)
            """, (first_admin_username, first_admin_email, hashed_password))
            
            conn.commit()
            logging.info("First admin user created successfully.")
        else:
            logging.info("Admin user already exists.")
    except Exception as e:
        logging.error(f"An error occurred during database setup: {e}")
    finally:
        cursor.close()
        conn.close()
    
    logging.info(" Konfiguracja bazy danych zakończona!")
