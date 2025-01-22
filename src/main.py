from src.auth.authenticate_user import authenticate_user
from src.handlers.execute_action import execute_action
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to the Database Manager!")

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
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            logging.info("Exiting program. Goodbye!")
            break

        # Execute the chosen action
        execute_action(choice)

if __name__ == "__main__":
    main()