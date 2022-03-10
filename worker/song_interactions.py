from creds import db
from models import liked_songs, song_list
import sqlalchemy as sql


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
