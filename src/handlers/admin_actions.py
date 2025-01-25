import logging
from handlers.data_operations import fetch_data, update_data, delete_data, get_like_count
from db.connect_db import connect_to_db
from auth.encryption import hash_password  # Add this import

def execute_admin_action(choice, table_name=None, data=None):
    if choice == "1":
        data = fetch_data(table_name)
        print(data)
    elif choice == "2":
        pass  # Remove add_data functionality
    elif choice == "3":
        record_id = data.pop('id')
        update_data(table_name, record_id, data)
    elif choice == "4":
        delete_data(table_name, data)
    elif choice == "5":
        entity = table_name.strip().lower()
        entity_id = int(data)
        likes = get_like_count(entity, entity_id)
        if likes is not None:
            print(f" {entity} with ID {entity_id} has {likes} likes.")
    else:
        logging.error("Invalid choice. Please try again.")

def add_user(username, email, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    hashed_password = hash_password(password)  # Hash the password
    try:
        cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        logging.info(f"User {username} added successfully.")
    except Exception as e:
        logging.error(f"An error occurred while adding the user: {e}")
    finally:
        cursor.close()
        conn.close()

def add_artist(name, email, password, country_id=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    hashed_password = hash_password(password)  # Hash the password
    try:
        cursor.execute("INSERT INTO artists (name, email, hashed_password, id_country) VALUES (?, ?, ?, ?)", (name, email, hashed_password, country_id))
        conn.commit()
        logging.info(f"Artist {name} added successfully.")
    except Exception as e:
        logging.error(f"An error occurred while adding the artist: {e}")
    finally:
        cursor.close()
        conn.close()
