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


## 3. Project Structure

```
spotify-database-project/
├── .env
├── README.md
├── database.sql
├── environment.yml
├── requirements.txt
└── src/
    ├── connect_db.py
    └── utils/
        └── encryption.py
```

- `.env`: Environment variables for database connection.
- `README.md`: Project documentation.
- `database.sql`: SQL script to create the database schema.
- `environment.yml`: Conda environment configuration.
- `requirements.txt`: Python dependencies.
- `src/`: Source code directory.
  - `connect_db.py`: Script to connect to the database.
  - `utils/encryption.py`: Utility for password hashing.
