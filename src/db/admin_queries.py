from src.db.connect_db import connect_to_db

def get_like_count(entity_type, entity_id):

    # Zwraca liczbę polubień dla utworu, albumu lub artysty.

    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            if entity_type == "song":
                cursor.execute("SELECT count_song_likes(%s)", (entity_id,))
            elif entity_type == "album":
                cursor.execute("SELECT count_album_likes(%s)", (entity_id,))
            elif entity_type == "artist":
                cursor.execute("SELECT count_artist_likes(%s)", (entity_id,))
            else:
                print("Niepoprawny typ! Wybierz: song, album, artist.")
                return None

            like_count = cursor.fetchone()[0]
            return like_count
        except Exception as e:
            print(f"Błąd pobierania polubień: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    entity = input("Podaj typ (song/album/artist): ").strip().lower()
    entity_id = int(input("Podaj ID: "))
    likes = get_like_count(entity, entity_id)
    if likes is not None:
        print(f"{entity} o ID {entity_id} ma {likes} polubień!")
