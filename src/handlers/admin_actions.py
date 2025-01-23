import logging
from handlers.data_operations import fetch_data, add_data, update_data, delete_data, get_like_count
from db.connect_db import connect_to_db

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
    else:
        logging.error("Invalid choice. Please try again.")
