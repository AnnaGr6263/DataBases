import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QInputDialog, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QSizePolicy, QDialog, QFormLayout, QDialogButtonBox
from auth.authenticate_user import authenticate_user
from handlers.user_actions import execute_user_action
from handlers.artist_actions import execute_artist_action
from handlers.admin_actions import execute_admin_action
from handlers.data_operations import get_like_count, add_data
from db.setup_db import setup_database
from db.connect_db import connect_to_db
import logging
from dotenv import load_dotenv
from auth.encryption import hash_password

class DatabaseManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.menu_windows = []  # Keep references to menu windows

    def initUI(self):
        load_dotenv()  # Load environment variables from .env file
        logging.basicConfig(level=logging.INFO)
        logging.info("Welcome to the Database Manager!")

        # AUTOMATYCZNA KONFIGURACJA BAZY PRZY STARCIE
        try:
            setup_database()
        except Exception as e:
            logging.error(f"An error occurred while setting up the database: {e}")
            return

        self.setWindowTitle('Database Manager')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel('Enter your username:')
        layout.addWidget(self.username_label)

        self.username_entry = QLineEdit(self)
        layout.addWidget(self.username_entry)

        self.password_label = QLabel('Enter your password:')
        layout.addWidget(self.password_label)

        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.user_button = QPushButton('Login as User', self)
        self.user_button.clicked.connect(lambda: self.login('user'))
        layout.addWidget(self.user_button)

        self.admin_button = QPushButton('Login as Admin', self)
        self.admin_button.clicked.connect(lambda: self.login('admin'))
        layout.addWidget(self.admin_button)

        self.artist_button = QPushButton('Login as Artist', self)
        self.artist_button.clicked.connect(lambda: self.login('artist'))
        layout.addWidget(self.artist_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def login(self, user_type):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if authenticate_user(username, password, user_type):
            if user_type == 'user':
                self.user_menu(username)
            elif user_type == 'admin':
                self.admin_menu()
            elif user_type == 'artist':
                self.artist_menu(username)
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid credentials. Please try again.")

    def user_menu(self, username):
        manage_window = QWidget()
        manage_window.setWindowTitle("User Menu")
        manage_window.setGeometry(100, 100, 800, 600)  # Set default size

        layout = QVBoxLayout()  # Change to QVBoxLayout to add buttons on top

        button_layout = QHBoxLayout()  # Layout for add, delete, filter, and exit buttons
        button_layout.setSpacing(5)  # Set spacing to 5 for consistency

        filter_input = QLineEdit(manage_window)
        filter_input.setPlaceholderText("Enter filter text")
        button_layout.addWidget(filter_input)

        filter_button = QPushButton("Filter", manage_window)
        filter_button.setFixedWidth(60)  # Set fixed width for top buttons
        filter_button.clicked.connect(lambda: self.filter_data(filter_input.text()))
        button_layout.addWidget(filter_button)

        exit_button = QPushButton("Exit", manage_window)
        exit_button.setFixedWidth(60)  # Set fixed width for top buttons
        exit_button.clicked.connect(manage_window.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)  # Add button layout to the top

        table_layout = QHBoxLayout()  # Layout for table and side buttons

        side_button_layout = QVBoxLayout()
        side_button_layout.setSpacing(3)  # Reduce spacing between buttons to one-third

        self.table_buttons = ["songs", "playlists", "albums", "favorite_artists", "liked_songs", "subscription_info", "artists"]
        for table in self.table_buttons:
            button = QPushButton(table.replace('_', ' ').capitalize(), manage_window)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Make buttons expand vertically
            button.setFixedWidth(125)  # Set fixed width for buttons
            button.clicked.connect(lambda _, t=table: self.load_table_data(t, username))
            side_button_layout.addWidget(button)

        table_layout.addLayout(side_button_layout, 1)  # Add side button layout with stretch factor 1

        self.table_widget = QTableWidget(manage_window)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Make columns resizable
        self.table_widget.verticalHeader().setVisible(False)  # index column not visible
        table_layout.addWidget(self.table_widget, 4)  # Add table widget with stretch factor 4

        layout.addLayout(table_layout)  # Add table layout to the main layout

        manage_window.setLayout(layout)
        manage_window.show()
        self.menu_windows.append(manage_window)  # Keep reference

        self.load_table_data(self.table_buttons[0], username)  # Load the first table by default

    def admin_menu(self):
        self.manage_data()  # Skip directly to the tables view

    def manage_data(self):
        manage_window = QWidget()
        manage_window.setWindowTitle("Manage Data")
        manage_window.setGeometry(100, 100, 800, 600)  # Set default size

        layout = QVBoxLayout()  # Change to QVBoxLayout to add buttons on top

        button_layout = QHBoxLayout()  # Layout for add, delete, filter, and exit buttons
        button_layout.setSpacing(5)  # Set spacing to 5 for consistency

        add_button = QPushButton("Add", manage_window)
        add_button.setFixedWidth(60)  # Set fixed width for top buttons
        add_button.clicked.connect(self.add_data)  # TODO: Implement add_data functionality
        button_layout.addWidget(add_button)

        delete_button = QPushButton("Delete", manage_window)
        delete_button.setFixedWidth(60)  # Set fixed width for top buttons
        delete_button.clicked.connect(self.delete_data)
        button_layout.addWidget(delete_button)

        filter_input = QLineEdit(manage_window)
        filter_input.setPlaceholderText("Enter filter text")
        button_layout.addWidget(filter_input)

        filter_button = QPushButton("Filter", manage_window)
        filter_button.setFixedWidth(60)  # Set fixed width for top buttons
        filter_button.clicked.connect(lambda: self.filter_data(filter_input.text()))
        button_layout.addWidget(filter_button)

        exit_button = QPushButton("Exit", manage_window)
        exit_button.setFixedWidth(60)  # Set fixed width for top buttons
        exit_button.clicked.connect(manage_window.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)  # Add button layout to the top

        table_layout = QHBoxLayout()  # Layout for table and side buttons

        side_button_layout = QVBoxLayout()
        side_button_layout.setSpacing(3)  # Reduce spacing between buttons to one-third

        self.table_buttons = [
            "users", "admins", "countries", "artists", "genres", "albums", "songs", "playlists",
            "playlist_songs", "subscriptions", "song_stats", "song_likes", "album_likes", "artist_likes", "admin_created_playlists"
        ]
        for table in self.table_buttons:
            button = QPushButton(table.replace('_', ' ').capitalize(), manage_window)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Make buttons expand vertically
            button.setFixedWidth(125)  # Set fixed width for buttons
            button.clicked.connect(lambda _, t=table: self.load_table_data(t))
            side_button_layout.addWidget(button)

        table_layout.addLayout(side_button_layout, 1)  # Add side button layout with stretch factor 1

        self.table_widget = QTableWidget(manage_window)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Make columns resizable
        self.table_widget.verticalHeader().setVisible(False)  # index column not visible
        table_layout.addWidget(self.table_widget, 4)  # Add table widget with stretch factor 4

        layout.addLayout(table_layout)  # Add table layout to the main layout

        manage_window.setLayout(layout)
        manage_window.show()
        self.menu_windows.append(manage_window)  # Keep reference

        self.load_table_data(self.table_buttons[0])  # Load the first table by default

    def add_data(self, table_name=None, skip_table_choice=False):
        add_dialog = QDialog(self)
        add_dialog.setWindowTitle("Add Data")
        add_dialog.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        if skip_table_choice:
            # Skip table field and forcibly use current_table_name
            current_table = table_name
        else:
            table_label = QLabel("Select table to add data:")
            layout.addWidget(table_label)

            table_combo = QComboBox()
            table_combo.addItems([
                "users", "admins", "countries", "artists", "genres", "albums", "songs", "playlists",
                "playlist_songs", "subscriptions", "song_stats", "song_likes", "album_likes", "artist_likes", "admin_created_playlists"
            ])
            layout.addWidget(table_combo)

            if table_name:
                table_combo.setCurrentText(table_name)
                table_combo.setEnabled(False)

            current_table = table_combo.currentText()

        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)

        self.success_label = QLabel("")
        layout.addWidget(self.success_label)

        def update_form_fields(table):
            while self.form_layout.count():
                child = self.form_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            if table == "users":
                self.form_layout.addRow("Username:", QLineEdit())
                self.form_layout.addRow("Email:", QLineEdit())
                self.form_layout.addRow("Password:", QLineEdit())
            elif table == "admins":
                self.form_layout.addRow("Username:", QLineEdit())
                self.form_layout.addRow("Email:", QLineEdit())
                self.form_layout.addRow("Password:", QLineEdit())
            elif table == "countries":
                self.form_layout.addRow("Name:", QLineEdit())
            elif table == "artists":
                self.form_layout.addRow("Name:", QLineEdit())
                self.form_layout.addRow("Email:", QLineEdit())
                self.form_layout.addRow("Password:", QLineEdit())
                self.form_layout.addRow("Country:", QLineEdit())  # Changed to ask for country name
            elif table == "genres":
                self.form_layout.addRow("Name:", QLineEdit())
            elif table == "albums":
                self.form_layout.addRow("Title:", QLineEdit())
                if not skip_table_choice:
                    self.form_layout.addRow("Artist:", QLineEdit())  # Changed to ask for artist name
                self.form_layout.addRow("Genre:", QLineEdit())  # Changed to ask for genre name
                self.form_layout.addRow("Release Year:", QLineEdit())
            elif table == "songs":
                self.form_layout.addRow("Title:", QLineEdit())
                self.form_layout.addRow("Duration:", QLineEdit())
                self.form_layout.addRow("Album:", QLineEdit())  # Changed to ask for album title
                self.form_layout.addRow("Genre:", QLineEdit())  # Changed to ask for genre name
            elif table == "playlists":
                self.form_layout.addRow("Name:", QLineEdit())
                self.form_layout.addRow("User:", QLineEdit())  # Changed to ask for username
                self.form_layout.addRow("Is Public:", QLineEdit())
            elif table == "playlist_songs":
                self.form_layout.addRow("Playlist:", QLineEdit())  # Changed to ask for playlist name
                self.form_layout.addRow("Song:", QLineEdit())  # Changed to ask for song title
            elif table == "subscriptions":
                self.form_layout.addRow("User:", QLineEdit())  # Changed to ask for username
                self.form_layout.addRow("Start Date:", QLineEdit())
                self.form_layout.addRow("End Date:", QLineEdit())
            elif table == "song_stats":
                self.form_layout.addRow("Song:", QLineEdit())  # Changed to ask for song title
                self.form_layout.addRow("Play Count:", QLineEdit())
                self.form_layout.addRow("Last Played:", QLineEdit())
            elif table == "song_likes":
                self.form_layout.addRow("User:", QLineEdit())  # Changed to ask for username
                self.form_layout.addRow("Song:", QLineEdit())  # Changed to ask for song title
            elif table == "album_likes":
                self.form_layout.addRow("User:", QLineEdit())  # Changed to ask for username
                self.form_layout.addRow("Album:", QLineEdit())  # Changed to ask for album title
            elif table == "artist_likes":
                self.form_layout.addRow("User:", QLineEdit())  # Changed to ask for username
                self.form_layout.addRow("Artist:", QLineEdit())  # Changed to ask for artist name
            elif table == "admin_created_playlists":
                self.form_layout.addRow("Playlist:", QLineEdit())  # Changed to ask for playlist name
                self.form_layout.addRow("Admin:", QLineEdit())  # Changed to ask for admin username

        if not skip_table_choice:
            table_combo.currentTextChanged.connect(update_form_fields)
            update_form_fields(table_combo.currentText())
        else:
            update_form_fields(current_table)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.submit_add_data(current_table, self.form_layout))
        button_box.rejected.connect(add_dialog.reject)
        layout.addWidget(button_box)

        add_dialog.setLayout(layout)
        add_dialog.exec_()

    def submit_add_data(self, table_name, form_layout):
        data = {}
        for i in range(form_layout.rowCount()):
            label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
            field_item = form_layout.itemAt(i, QFormLayout.FieldRole)
            if label_item and field_item:
                label = label_item.widget().text().replace(":", "")
                value = field_item.widget().text()
                if label.lower() == "password":
                    label = "hashed_password"
                    value = hash_password(value)
                data[label] = value

        # If artist is adding data for "albums" or "songs" and the form has no "Artist", fill it automatically
        if table_name in ["albums", "songs"] and "Artist" not in data:
            data["Artist"] = self.username_entry.text()

        add_data(table_name, data)
        self.load_table_data(table_name)
        self.success_label.setText("Data added successfully!")
        print(f"Adding data to {table_name}: {data}")

    def delete_data(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Delete Data", "No item selected.")
            return

        row = selected_items[0].row()
        record_id = self.table_widget.item(row, 0).text()  # Assuming the first column is the ID
        table_name = self.current_table_name  # Use the current table name

        execute_admin_action("4", table_name, record_id)
        self.load_table_data(table_name)

    def load_table_data(self, table_name, username=None):
        self.current_table_name = table_name  # Store the current table name
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                if table_name in ["favorite_artists", "liked_songs", "subscription_info"]:
                    cursor.execute(f"SELECT id_user FROM users WHERE username = %s", (username,))
                    user_id = cursor.fetchone()[0]
                    if table_name == "favorite_artists":
                        cursor.execute(f"SELECT * FROM artist_likes WHERE id_user = %s", (user_id,))
                    elif table_name == "liked_songs":
                        cursor.execute(f"SELECT * FROM song_likes WHERE id_user = %s", (user_id,))
                    elif table_name == "subscription_info":
                        cursor.execute(f"SELECT * FROM subscriptions WHERE id_user = %s", (user_id,))
                else:
                    cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                if username and "hashed_password" in columns:
                    hashed_password_index = columns.index("hashed_password")
                    columns.pop(hashed_password_index)
                    for row in data:
                        row.pop(hashed_password_index)

                self.table_widget.setRowCount(len(data))
                self.table_widget.setColumnCount(len(columns))
                self.table_widget.setHorizontalHeaderLabels(columns)

                for row_idx, row_data in enumerate(data):
                    for col_idx, col_data in enumerate(row_data):
                        self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            except Exception as e:
                logging.error(f"Error loading table data from {table_name}: {e}")
            finally:
                cursor.close()
                connection.close()

    def filter_data(self, filter_text):
        # TODO: Implement filter_data functionality
        pass

    def check_likes(self):
        entity, ok = QInputDialog.getText(self, "Input", "Enter type (song/album/artist):")
        if ok:
            entity_id, ok = QInputDialog.getInt(self, "Input", "Enter ID:")
            if ok:
                likes = get_like_count(entity.strip().lower(), entity_id)
                if likes is not None:
                    QMessageBox.information(self, "Likes", f"{entity} with ID {entity_id} has {likes} likes.")

    def execute_admin_action(self, choice):
        execute_admin_action(choice)

    def artist_menu(self, username):
        manage_window = QWidget()
        manage_window.setWindowTitle("Artist Menu")
        manage_window.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        add_button = QPushButton("Add", manage_window)
        add_button.setFixedWidth(60)
        add_button.clicked.connect(lambda: self.add_data(self.current_table_name, skip_table_choice=True))
        button_layout.addWidget(add_button)

        delete_button = QPushButton("Delete", manage_window)
        delete_button.setFixedWidth(60)
        delete_button.clicked.connect(lambda: self.delete_data())
        button_layout.addWidget(delete_button)

        filter_input = QLineEdit(manage_window)
        filter_input.setPlaceholderText("Enter filter text")
        button_layout.addWidget(filter_input)

        filter_button = QPushButton("Filter", manage_window)
        filter_button.setFixedWidth(60)
        filter_button.clicked.connect(lambda: self.filter_data(filter_input.text()))
        button_layout.addWidget(filter_button)

        exit_button = QPushButton("Exit", manage_window)
        exit_button.setFixedWidth(60)
        exit_button.clicked.connect(manage_window.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        table_layout = QHBoxLayout()
        side_button_layout = QVBoxLayout()
        side_button_layout.setSpacing(3)

        self.table_buttons = ["songs", "albums"]
        for table in self.table_buttons:
            button = QPushButton(table.capitalize(), manage_window)
            button.setFixedWidth(125)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            button.clicked.connect(lambda _, t=table: self.load_artist_table_data(t, username))
            side_button_layout.addWidget(button)

        table_layout.addLayout(side_button_layout, 1)

        self.table_widget = QTableWidget(manage_window)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        table_layout.addWidget(self.table_widget, 4)

        layout.addLayout(table_layout)
        manage_window.setLayout(layout)
        manage_window.show()
        self.menu_windows.append(manage_window)

        self.current_table_name = self.table_buttons[0]
        self.load_artist_table_data(self.current_table_name, username)

    def load_artist_table_data(self, table_name, username):
        self.current_table_name = table_name
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT id_artist FROM artists WHERE name = %s", (username,))
                artist_id = cursor.fetchone()[0]
                if table_name == "songs":
                    cursor.execute("""
                        SELECT s.*
                        FROM songs s
                        JOIN albums a ON s.id_album = a.id_album
                        WHERE a.id_artist = %s
                    """, (artist_id,))
                elif table_name == "albums":
                    cursor.execute("SELECT * FROM albums WHERE id_artist = %s", (artist_id,))
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                self.table_widget.setRowCount(len(data))
                self.table_widget.setColumnCount(len(columns))
                self.table_widget.setHorizontalHeaderLabels(columns)
                
                for row_idx, row_data in enumerate(data):
                    for col_idx, col_data in enumerate(row_data):
                        self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            except Exception as e:
                logging.error(f"Error loading table data: {e}")
            finally:
                cursor.close()
                connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DatabaseManagerApp()
    ex.show()
    sys.exit(app.exec_())
