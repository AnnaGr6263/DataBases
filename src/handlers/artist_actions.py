import logging
from handlers.data_operations import fetch_data, add_data, update_data, delete_data

def add_song(artist_id, title, duration, album_id, genre_id):
    data = {
        "title": title,
        "duration": duration,
        "id_album": album_id,
        "id_genre": genre_id,
        "id_artist": artist_id
    }
    add_data("songs", data)

def view_songs(artist_id):
    songs = fetch_data("songs")
    artist_songs = [song for song in songs if song['id_artist'] == artist_id]
    print(artist_songs)

def view_albums(artist_id):
    albums = fetch_data("albums")
    artist_albums = [album for album in albums if album['id_artist'] == artist_id]
    print(artist_albums)

def update_song(song_id, title, duration, album_id, genre_id):
    data = {
        "title": title,
        "duration": duration,
        "id_album": album_id,
        "id_genre": genre_id
    }
    update_data("songs", song_id, data)

def delete_song(song_id):
    delete_data("songs", song_id)

def update_album(album_id, title, genre_id, release_year):
    data = {
        "title": title,
        "id_genre": genre_id,
        "release_year": release_year
    }
    update_data("albums", album_id, data)

def delete_album(album_id):
    delete_data("albums", album_id)

def execute_artist_action(choice, artist_id):
    if choice == "1":
        view_songs(artist_id)
    elif choice == "2":
        view_albums(artist_id)
    elif choice == "3":
        title = input("Enter song title: ")
        duration = input("Enter song duration (HH:MM:SS): ")
        album_id = int(input("Enter album ID: "))
        genre_id = int(input("Enter genre ID: "))
        add_song(artist_id, title, duration, album_id, genre_id)
    elif choice == "4":
        song_id = int(input("Enter song ID: "))
        title = input("Enter new song title: ")
        duration = input("Enter new song duration (HH:MM:SS): ")
        album_id = int(input("Enter new album ID: "))
        genre_id = int(input("Enter new genre ID: "))
        update_song(song_id, title, duration, album_id, genre_id)
    elif choice == "5":
        song_id = int(input("Enter song ID: "))
        delete_song(song_id)
    elif choice == "6":
        album_id = int(input("Enter album ID: "))
        title = input("Enter new album title: ")
        genre_id = int(input("Enter new genre ID: "))
        release_year = int(input("Enter new release year: "))
        update_album(album_id, title, genre_id, release_year)
    elif choice == "7":
        album_id = int(input("Enter album ID: "))
        delete_album(album_id)
    else:
        logging.error("Invalid choice. Please try again.")
