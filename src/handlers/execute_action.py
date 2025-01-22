from src.handlers.data_handling import *
import logging

def execute_action(choice):
    """
    Executes an action based on the user's choice.
    """
    if choice == "1":
        data = view_data()
        for row in data:
            print(row)
    elif choice == "2":
        data = {
            'column1': input("Enter value for column1: "),
            'column2': input("Enter value for column2: ")
        }
        add_data(data)
    elif choice == "3":
        data = {
            'column1': input("Enter new value for column1: "),
            'column2': input("Enter value for column2 to update: ")
        }
        update_data(data)
    elif choice == "4":
        data = {
            'column1': input("Enter value for column1 to delete: ")
        }
        delete_data(data)
    else:
        logging.warning("Invalid choice. Please try again.")
