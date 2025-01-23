from src.auth.authenticate_user import authenticate_user
from src.handlers.user_actions import execute_user_action
from src.handlers.artist_actions import execute_artist_action
from src.handlers.admin_actions import execute_admin_action
from src.handlers.data_operations import get_like_count
from src.db.setup_db import setup_database
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to the Database Manager!")

    # AUTOMATYCZNA KONFIGURACJA BAZY PRZY STARCIE
    try:
        setup_database()
    except Exception as e:
        logging.error(f"An error occurred while setting up the database: {e}")
        return

    while True:
        # Display login options
        print("\nLogin as:")
        print("1. User")
        print("2. Admin")
        print("3. Artist")
        print("4. Exit")

        login_choice = input("Enter your choice (1-4): ")

        if login_choice == "4":
            logging.info("Exiting program. Goodbye!")
            break

        # Authenticate user
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if not authenticate_user(username, password):
            logging.error("Invalid credentials. Please try again.")
            continue

        logging.info(f"Welcome, {username}!")

        if login_choice == "1":
            user_menu(username)
        elif login_choice == "2":
            admin_menu()
        elif login_choice == "3":
            artist_menu(username)

def user_menu(username):
    while True:
        # Display user menu options
        print("\nWhat would you like to do?")
        print("1. View songs")
        print("2. View playlists")
        print("3. View albums")
        print("4. View favorite artists")
        print("5. View liked songs")
        print("6. View subscription info")
        print("7. View artists")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == "8":
            logging.info("Exiting user menu. Goodbye!")
            break

        # Execute the chosen action
        execute_user_action(choice, username)

def admin_menu():
    while True:
        # Display admin menu options
        print("\nWhat would you like to do?")
        print("1. View data")
        print("2. Add data")
        print("3. Update data")
        print("4. Delete data")
        print("5. Check likes")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "5":
            entity = input("Enter type (song/album/artist): ").strip().lower()
            entity_id = int(input("Enter ID: "))
            likes = get_like_count(entity, entity_id)
            if likes is not None:
                print(f" {entity} with ID {entity_id} has {likes} likes.")

        if choice == "6":
            logging.info("Exiting admin menu. Goodbye!")
            break

        # Execute the chosen action
        execute_admin_action(choice)

def artist_menu(artist_id):
    while True:
        # Display artist menu options
        print("\nWhat would you like to do?")
        print("1. View songs")
        print("2. View albums")
        print("3. Add song")
        print("4. Update song")
        print("5. Delete song")
        print("6. Update album")
        print("7. Delete album")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == "8":
            logging.info("Exiting artist menu. Goodbye!")
            break

        # Execute the chosen action
        execute_artist_action(choice, artist_id)

if __name__ == "__main__":
    main()