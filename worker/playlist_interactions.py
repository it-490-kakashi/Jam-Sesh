from creds import db
from models import song_list, playlist, playlist_content
from song_interactions import find_song_by_id
import logging

logging.basicConfig(filename='log_file.log', encoding='utf-8', format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Playlist CRUD
def new_playlist(name, user_id):
    # Connect to db
    with db.connect() as conn:
        # Make new playlist record with name and user_id
        new_playlist = playlist.insert().values(playlist_name=name,
                                                user_id=user_id)
        # Execute new record
        conn.execute(new_playlist)
        logging.debug("Made new playlist for user")
        return f"Made new playlist for user:{user_id}"


def get_user_playlists(user_id):
    with db.connect() as conn:
        user_playlists = playlist.select().where(playlist.c.user_id == user_id)
        return conn.execute(user_playlists).fetchall()


def update_playlist_name(playlist_id, new_name, user_id):
    with db.connect() as conn:
        if user_owns_playlist(playlist_id, user_id):
            update = playlist.update().where(playlist.c.id == playlist_id).values(playlist_name=new_name)
            conn.execute(update)
            return True
        return False


def delete_playlist(playlist_id, user_id):
    with db.connect() as conn:
        if user_owns_playlist(playlist_id, user_id):
            conn.execute(playlist.delete().where(playlist.c.id == playlist_id, playlist.c.user_id == user_id))
            logging.debug("Deleted Playlist")
            return f"Deleted Playlist @ id:{playlist_id}"
        logging.error("Playlist not found or owned")
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
        query = playlist_content.select().where(playlist_content.c.playlist_id == playlist_id)
        result = conn.execute(query).fetchall()
        lst = []
        for song_id in result:
            query = song_list.select().where(song_list.c.genius_id == song_id[1])
            lst.append(conn.execute(query).fetchone())
        return lst


def add_song_to_playlist(song_id, playlist_id, user_id):
    with db.connect() as conn:
        if user_owns_playlist(playlist_id, user_id) and find_song_by_id(song_id):
            try:
                query = playlist_content.insert().values(playlist_id=playlist_id,
                                                         song_id=song_id)
                conn.execute(query)
            except:
                return False
            return True
        return False


def remove_song_from_playlist(song_id, playlist_id, user_id):
    with db.connect() as conn:
        if is_song_in_playlist(song_id, playlist_id) & user_owns_playlist(playlist_id, user_id):
            query = playlist_content.delete().where(playlist_content.c.playlist_id == playlist_id,
                                                    playlist_content.c.song_id == song_id)
            conn.execute(query)
            logging.debug("Delete song from playlist")
            return f"Delete song @ id:{song_id} from playlist @ id:{playlist_id}"
        logging.error("Song not in playlist")
        return f"Song @ id:{song_id} is not in playlist @ id:{playlist_id} or playlist not owned by user"


def is_song_in_playlist(song_id, playlist_id):
    with db.connect() as conn:
        query = playlist_content.select().where(playlist_content.c.playlist_id == playlist_id,
                                                playlist_content.c.song_id == song_id)
        return conn.execute(query).fetchone() is not None  # Returns true if playlist is not None
