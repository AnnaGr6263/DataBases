import logging
from db.connect_db import connect_to_db

def fetch_data(table_name):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()
            logging.info(f"Fetched data from {table_name}: {result}")
            return result
        except Exception as e:
            logging.error(f"Error fetching data from {table_name}: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

def get_singular_form(table_name):
    if table_name.endswith('ies'):
        return table_name[:-3] + 'y'
    elif table_name.endswith('s') and not table_name.endswith('ss'):
        return table_name[:-1]
    return table_name

def get_or_create_id(table_name, column_name, value, additional_data=None):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            singular_form = get_singular_form(table_name)
            # Check if the value already exists
            cursor.execute(f"SELECT id_{singular_form} FROM {table_name} WHERE {column_name} = %s", (value,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                # Insert the new value and return the new ID
                if additional_data:
                    columns = ', '.join([column_name] + list(additional_data.keys()))
                    placeholders = ', '.join(['%s'] * (len(additional_data) + 1))
                    values = [value] + list(additional_data.values())
                    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
                else:
                    cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (%s)", (value,))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            logging.error(f"Error getting or creating ID in {table_name}: {e}")
        finally:
            cursor.close()
            connection.close()

def add_data(table_name, data):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            # Convert form labels to match database column names
            data = {key.lower().replace(' ', '_'): value for key, value in data.items()}

            # Handle foreign key lookups or inserts
            foreign_keys = {
                "country": "countries",
                "genre": "genres",
                "artist": "artists",
                "album": "albums",
                "user": "users",
                "admin": "admins",
                "playlist": "playlists",
                "song": "songs"
            }
            for key, table in foreign_keys.items():
                if key in data and not data[key].isdigit():
                    additional_data = None
                    if key == "artist":
                        additional_data = {"email": data.get("email", ""), "hashed_password": data.get("hashed_password", ""), "id_country": get_or_create_id("countries", "name", data.get("country", ""))}
                    elif key == "album":
                        additional_data = {"id_artist": get_or_create_id("artists", "name", data.get("artist", ""))}
                    data[f"id_{key}"] = get_or_create_id(table, "name", data[key], additional_data)
                    del data[key]

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
