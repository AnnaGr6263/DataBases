import logging
from handlers.data_operations import fetch_data

def execute_user_action(choice, username):
    if choice == "1":
        songs = fetch_data("songs")
        print(songs)
    elif choice == "2":
        playlists = fetch_data("playlists")
        print(playlists)
    elif choice == "3":
        albums = fetch_data("albums")
        print(albums)
    elif choice == "4":
        favorite_artists = fetch_data("artist_likes")
        print(favorite_artists)
    elif choice == "5":
        liked_songs = fetch_data("song_likes")
        print(liked_songs)
    elif choice == "6":
        subscriptions = fetch_data("subscriptions")
        print(subscriptions)
    elif choice == "7":
        artists = fetch_data("artists")
        print(artists)
    else:
        logging.error("Invalid choice. Please try again.")
