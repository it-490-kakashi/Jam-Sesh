from creds import db
from models import liked_songs, song_list
import sqlalchemy as sql


# Likes system
def get_liked_songs(songs_list, user_id):
    with db.connect() as conn:
        results = {}
        for song in songs_list:
            result = liked_songs.select().where(liked_songs.c.song_id == song, liked_songs.c.user_id == user_id)
            result = conn.execute(result).fetchone()
            if result is not None:
                results[song] = True
            else:
                results[song] = False
        return results


def get_liked_song(song_id, user_id):
    with db.connect() as conn:
        result = liked_songs.select().where(liked_songs.c.song_id == song_id, liked_songs.c.user_id == user_id)
        result = conn.execute(result).fetchone()
        return result is not None  # Returns True if there is a song


def like_song(song_id, user_id):
    with db.connect() as conn:
        if not get_liked_song(song_id, user_id):
            query = liked_songs.insert().values(song_id=song_id, user_id=user_id)
            conn.execute(query)
            return f"Added {song_id} for {user_id}"
        return f"User already likes song @ id:{song_id}"


def dislike_song(song_id, user_id):
    with db.connect() as conn:
        if get_liked_song(song_id, user_id):
            conn.execute(liked_songs.delete().where(liked_songs.c.song_id == song_id, liked_songs.c.user_id == user_id))
            return f"Disliked song @ id:{song_id} for user:{user_id}"
        return "This user hasn't liked this song"


# Song interactions
def add_song(name, artist, genre, genius_id):
    with db.connect() as conn:
        insert = song_list.insert().values(
            name=name,
            artist=artist,
            genre=genre,
            genius_id=genius_id
        )
        conn.execute(insert)


def find_song(name, artist):
    with db.connect() as conn:
        select = song_list.select().where(song_list.c.name == name, song_list.c.artist == artist)
        result = conn.execute(select)
        if len(result.fetchall()) > 0:
            return True
        else:
            return False


def find_song_by_id(song_id):
    with db.connect() as conn:
        query = song_list.select().where(song_list.c.genius_id == song_id)
        result = conn.execute(query)
        return len(result.fetchall()) > 0
