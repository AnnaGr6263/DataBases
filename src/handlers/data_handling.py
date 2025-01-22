import logging
from src.db.connect_db import connect_to_db

def view_data():
    logging.info("Viewing data...")
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM your_table")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

def add_data(data):
    logging.info("Adding data...")
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", (data['column1'], data['column2']))
            connection.commit()
        except Exception as e:
            connection.rollback()
            logging.error(f"Error adding data: {e}")
        finally:
            cursor.close()
            connection.close()

def update_data(data):
    logging.info("Updating data...")
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE your_table SET column1 = %s WHERE column2 = %s", (data['column1'], data['column2']))
            connection.commit()
        except Exception as e:
            connection.rollback()
            logging.error(f"Error updating data: {e}")
        finally:
            cursor.close()
            connection.close()

def delete_data(data):
    logging.info("Deleting data...")
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM your_table WHERE column1 = %s", (data['column1'],))
            connection.commit()
        except Exception as e:
            connection.rollback()
            logging.error(f"Error deleting data: {e}")
        finally:
            cursor.close()
            connection.close()
