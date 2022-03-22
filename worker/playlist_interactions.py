from creds import db
from models import song_list, playlist, playlist_content


# Playlist CRUD
def new_playlist(name, user_id):
    # Connect to db
    with db.connect() as conn:
        # Make new playlist record with name and user_id
        new_playlist = playlist.insert().values(playlist_name=name,
                                                user_id=user_id)
        # Execute new record
        conn.execute(new_playlist)
        return f"Made new playlist for user:{user_id}"


def get_user_playlists(user_id):
    with db.connect() as conn:
        user_playlists = playlist.select().where(playlist.c.user_id == user_id)
        return conn.execute(user_playlists).fetchall()


def update_playlist_name(playlist_id, new_name):
    with db.connect() as conn:
        update = playlist.update().where(playlist.c.playlist_id == playlist_id).values(playlist_name=new_name)
        conn.execute(update)
        return f"Updated playlist:{playlist_id}"


def delete_playlist(playlist_id, user_id):
    with db.connect() as conn:
        if user_owns_playlist(playlist_id, user_id):
            conn.execute(playlist.delete().where(playlist.c.playlist_id == playlist_id, playlist.c.user_id == user_id))
            return f"Deleted Playlist @ id:{playlist_id}"
        return f"ERROR: Playlist @ id:{playlist_id} not found or not owned"


def playlist_exists(playlist_id):
    with db.connect() as conn:
        query = playlist.select().where(playlist.c.id == playlist_id)
        return conn.execute(query).fetchone() is not None  # Returns true if playlist is not None


def user_owns_playlist(playlist_id, user_id):
    with db.connect() as conn:
        query = playlist.select().where(playlist.c.id == playlist_id, playlist.c.user_id == user_id)
        return conn.execute(query).fetchone() is not None  # Returns true if playlist is not None


# Playlist content CRUD
def show_playlist_content(playlist_id):
    with db.connect() as conn:
        query = playlist_content.select.where(playlist_content.c.playlist_id == playlist_id)
        return conn.execute(query).fetchall()


def add_song_to_playlist(song_id, playlist_id, user_id):
    with db.connect() as conn:
        if user_owns_playlist(playlist_id, user_id):
            query = playlist_content.insert().values(playlist_id=playlist_id,
                                                     song_id=song_id)
            conn.execute(query)
            return f"Added song @ id:{song_id} to playlist @ id:{playlist_id}"
        return f"user @ id:{user_id} does not own playlist @ id:{playlist_id}"


def remove_song_from_playlist(song_id, playlist_id):
    with db.connect() as conn:
        if is_song_in_playlist(song_id, playlist_id):
            query = playlist_content.delete().where(playlist_content.c.playlist_id == playlist_id,
                                                    playlist_content.c.song_id == song_id)
            conn.execute(query)
            return f"Delete song @ id:{song_id} from playlist @ id:{playlist_id}"
        return f"Song @ id:{song_id} is not in playlist @ id:{playlist_id}"


def is_song_in_playlist(song_id, playlist_id):
    with db.connect() as conn:
        query = playlist_content.select().where(playlist_content.c.playlist_id == playlist_id,
                                                playlist_content.c.song_id == song_id)
        return conn.execute(query).fetchone() is not None  # Returns true if playlist is not None
