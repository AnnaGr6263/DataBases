# Spotify Database Project

This project is a relational database for a music streaming application similar to Spotify. It includes tables for users, artists, albums, songs, playlists, and more.

## Table of Contents

- [Spotify Database Project](#spotify-database-project)
  - [Table of Contents](#table-of-contents)
  - [1. Project Setup](#1-project-setup)
    - [1.1. Prerequisites](#11-prerequisites)
    - [1.2. Clone the Repository](#12-clone-the-repository)
    - [1.3. Set Up Conda Environment](#13-set-up-conda-environment)
    - [1.4. Configure Environment Variables](#14-configure-environment-variables)
    - [1.5. Run the Database Script](#15-run-the-database-script)
  - [2. Usage](#2-usage)
  - [3. Project Structure](#3-project-structure)

## 1. Project Setup

### 1.1. Prerequisites

- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- MariaDB server installed and running

### 1.2. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your_username/spotify-database-project.git
cd spotify-database-project
```

### 1.3. Set Up Conda Environment

Create and activate the Conda environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate spotifydb-env
```

### 1.4. Configure Environment Variables

Create a `.env` file in the root directory and add your database connection details:

```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

### 1.5. Run the Database Script

Run the database script to create the database schema:

```bash
mysql -u your_username -p your_database < database.sql
```

## 2. Usage

To run the main application, use the following command:

```bash
python src/main.py
```

## 3. Project Structure

```
spotify-database-project/
├── .env
├── README.md
├── database.sql
├── environment.yml
├── requirements.txt
└── src/
    ├── auth/
    │   ├── authenticate_user.py
    │   └── encryption.py
    ├── db/
    │   ├── connect_db.py
    │   └── fetch.py
    ├── handlers/
    │   ├── data_handling.py
    │   ├── execute_action.py
    │   └── user_handler.py
    └── main.py
```

- `.env`: Environment variables for database connection.
- `README.md`: Project documentation.
- `database.sql`: SQL script to create the database schema.
- `environment.yml`: Conda environment configuration.
- `requirements.txt`: Python dependencies.
- `src/`: Source code directory.
  - `auth/`: Authentication and encryption modules.
    - `authenticate_user.py`: Handles user authentication.
    - `encryption.py`: Utility for password hashing.
  - `db/`: Database connection and fetching modules.
    - `connect_db.py`: Script to connect to the database.
    - `fetch.py`: Script to fetch data from the database.
  - `handlers/`: Data handling and user input actions.
    - `data_handling.py`: Handles data operations.
    - `execute_action.py`: Handles user input actions.
    - `user_handler.py`: Handles user-related database operations.
  - `main.py`: Main entry point of the application.