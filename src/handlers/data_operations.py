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
        try:
            # Convert form labels to match database column names
            data = {key.lower().replace(' ', '_'): value for key, value in data.items()}
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            connection.commit()
            logging.info(f"Data added to {table_name} successfully.")
        except Exception as e:
            logging.error(f"Error adding data to {table_name}: {e}")
        finally:
            cursor.close()
            connection.close()

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
        try:
            # Determine the primary key column name based on the table name
            primary_key_column = f"id_{table_name[:-1]}"  # Remove the trailing 's' and prepend 'id_'
            sql = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
            cursor.execute(sql, (record_id,))
            connection.commit()
            logging.info(f"Data from {table_name} deleted successfully.")
        except Exception as e:
            logging.error(f"Error deleting data from {table_name}: {e}")
        finally:
            cursor.close()
            connection.close()

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
