from creds import db
from models import liked_songs


def get_liked_songs(song_list, user_id):
    with db.connect() as conn:
        result = []
        for song in song_list:
            operation = liked_songs.select().where(liked_songs.c.song_id == song, liked_songs.c.user_id == user_id)
            result.append(conn.execute(operation).fetchone())
        return result
