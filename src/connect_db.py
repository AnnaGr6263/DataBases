import mariadb
import sys
import os
from utils.encryption import hash_password

def connect_to_database():
    try:
        conn = mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            database=os.getenv("DB_NAME")
        )
        print("Connection successful!")
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def main():
    conn = connect_to_database()
    # Example usage of hash_password
    password = "your_password"
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")
    # ...existing code...
    conn.close()

if __name__ == "__main__":
    main()
