from src.handlers.data_handling import *
import logging

def execute_action(choice):
    """
    Executes an action based on the user's choice.
    """
    if choice == "1":
        view_data()
    elif choice == "2":
        add_data()
    elif choice == "3":
        update_data()
    elif choice == "4":
        delete_data()
    else:
        logging.warning("Invalid choice. Please try again.")
