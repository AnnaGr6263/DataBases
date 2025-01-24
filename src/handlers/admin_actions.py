import logging
from handlers.data_operations import fetch_data, add_data, update_data, delete_data, get_like_count
from db.connect_db import connect_to_db
from auth.encryption import hash_password  # Add this import

def execute_admin_action(choice):
    if choice == "1":
        table_name = input("Enter table name to view data: ")
        data = fetch_data(table_name)
        print(data)
    elif choice == "2":
        table_name = input("Enter table name to add data: ")
        data = input("Enter data to add (as a dictionary): ")
        add_data(table_name, eval(data))
    elif choice == "3":
        table_name = input("Enter table name to update data: ")
        record_id = int(input("Enter record ID to update: "))
        data = input("Enter new data (as a dictionary): ")
        update_data(table_name, record_id, eval(data))
    elif choice == "4":
        table_name = input("Enter table name to delete data: ")
        record_id = int(input("Enter record ID to delete: "))
        delete_data(table_name, record_id)
    elif choice == "5":
        entity = input("Enter type (song/album/artist): ").strip().lower()
        entity_id = int(input("Enter ID: "))
        likes = get_like_count(entity, entity_id)
        if likes is not None:
            print(f" {entity} with ID {entity_id} has {likes} likes.")
    elif choice == "6":
        username = input("Enter new username: ")
        email = input("Enter new email: ")
        password = input("Enter new password: ")
        add_user(username, email, password)
    elif choice == "7":
        name = input("Enter artist name: ")
        email = input("Enter artist email: ")
        password = input("Enter artist password: ")
        country_id = input("Enter country ID (optional): ")
        add_artist(name, email, password, country_id)
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
