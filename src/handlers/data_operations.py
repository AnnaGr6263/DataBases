import logging
from db.connect_db import connect_to_db

def fetch_data(table_name):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

def add_data(table_name, data):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        connection.commit()
        cursor.close()
        connection.close()
        logging.info(f"Data added to {table_name} successfully.")

def update_data(table_name, record_id, data):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
        cursor.execute(sql, list(data.values()) + [record_id])
        connection.commit()
        cursor.close()
        connection.close()
        logging.info(f"Data in {table_name} updated successfully.")

def delete_data(table_name, record_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        sql = f"DELETE FROM {table_name} WHERE id = %s"
        cursor.execute(sql, (record_id,))
        connection.commit()
        cursor.close()
        connection.close()
        logging.info(f"Data from {table_name} deleted successfully.")

def get_like_count(entity_type, entity_id):
    # Zwraca liczbę polubień dla utworu, albumu lub artysty.
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            if entity_type == "song":
                cursor.execute("SELECT count_song_likes(%s)", (entity_id,))
            elif entity_type == "album":
                cursor.execute("SELECT count_album_likes(%s)", (entity_id,))
            elif entity_type == "artist":
                cursor.execute("SELECT count_artist_likes(%s)", (entity_id,))
            else:
                print("Niepoprawny typ! Wybierz: song, album, artist.")
                return None

            like_count = cursor.fetchone()[0]
            return like_count
        except Exception as e:
            print(f"Błąd pobierania polubień: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
