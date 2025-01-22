from src.auth.authenticate_user import authenticate_user
from src.handlers.execute_action import execute_action
from src.db.admin_queries import get_like_count
from src.db.setup_db import setup_database
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to the Database Manager!")

    # AUTOMATYCZNA KONFIGURACJA BAZY PRZY STARCIE
    setup_database()

    # Authenticate user
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if not authenticate_user(username, password):
        logging.error("Invalid credentials. Exiting program.")
        return

    logging.info(f"Welcome, {username}!")

    while True:
        # Display menu options
        print("\nWhat would you like to do?")
        print("1. View data")
        print("2. Add data")
        print("3. Update data")
        print("4. Delete data")
        print("5. Check likes (Admin only)")
        print("6. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            entity = input("Enter type (song/album/artist): ").strip().lower()
            entity_id = int(input("Enter ID: "))
            likes = get_like_count(entity, entity_id)
            if likes is not None:
                print(f" {entity} with ID {entity_id} has {likes} likes.")

        if choice == "6":
            logging.info("Exiting program. Goodbye!")
            break

        # Execute the chosen action
        execute_action(choice)

if __name__ == "__main__":
    main()