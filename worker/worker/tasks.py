import time
import os
from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
from models import create_all
from basic_crud import *
from find_user import *
from user_interactions import *
from song_interactions import *
from playlist_interactions import *
from databaseseed import has_news, seed_news
from socialTasks import get_news_db
from dump_user import create_dump, retrieve_latest_dump
from run_tasks import run_jobs, add_jobs

load_dotenv()

logger = get_task_logger(__name__)

app = Celery('task',
             broker=os.getenv("BROKER_URL"),
             backend='db+postgresql+psycopg2://' + os.getenv("DATABASE_URL"))


# Creates tables
@app.task()
def create_db():
    create_all()
    add_jobs()
    run_jobs()

@app.task()
def get_latest_dump():
    return retrieve_latest_dump()

# User CRUD
# Create
@app.task()
def add_user(first_name, last_name, email, username, password):
    return add_user(first_name, last_name, email, username, password)


# Read
@app.task()
def get_users():
    return get_users()


# Read user @ id
@app.task()
def get_user(user_id):
    return get_user(user_id)


# Update first/last @ id
@app.task()
def update_user(user_id, first, last):
    return update_user(user_id, first, last)


# Delete
@app.task()
def delete_user(user_id):
    return delete_user(user_id)


# Authentication
@app.task()
def login(username, password):
    return login(username, password)


@app.task()
def register(username, first_name, last_name, email, password):
    return register(username, first_name, last_name, email, password)


@app.task()
def logout(session_token):
    return logout(session_token)


@app.task()
def token_valid(session_token):
    return user_session_valid(session_token)


@app.task()
def user_info_from_session_token(session_token):
    return user_info_from_session_token(session_token)


# User Methods
@app.task()
def find_user_by(method, params):
    if type(params) is not list or tuple:
        return "ERROR: params is not a list or tuple"

    if method == "id":
        return find_user.by_id(params[0])
    if method == "username":
        return find_user.by_username(params[0])
    if method == "first&last":
        return find_user.by_first_and_last(params[0], params[1])

    return False


# Like system functions
@app.task()
def get_liked_songs(song_list, user_id):
    return get_liked_songs(song_list, user_id)


@app.task()
def get_liked_song(song_id, user_id):
    return get_liked_song(song_id, user_id)


@app.task()
def like_song(genius_id, user_id):
    return like_song(genius_id, user_id)


@app.task()
def dislike_song(genius_id, user_id):
    return dislike_song(genius_id, user_id)


@app.task()
def add_song(name, artist, genre, genius_id):
    return add_song(name, artist, genre, genius_id)


@app.task()
def find_song(name, artist):
    return find_song(name, artist)

@app.task()
def update_views(genius_id):
    increaseView(genius_id)
    # to-do call increase views

@app.task()
def get_views(genius_id):
    return getView(genius_id)
    # Celery Test Code

@app.task()
def seed_if_empty():
    if not has_news():
        seed_news()

@app.task()
def get_news():
    return get_news_db()

# Playlist functions
@app.task()
def new_playlist(name, token):
    return new_playlist(name, user_info_from_session_token(token)[0])


@app.task()
def get_user_playlists(token):
    return get_user_playlists(user_info_from_session_token(token)[0])


@app.task()
def update_playlist_name(token, playlist_id, new_name):
    return update_playlist_name(playlist_id, new_name, user_info_from_session_token(token)[0])


@app.task()
def delete_playlist(playlist_id, token):
    return delete_playlist(playlist_id, user_info_from_session_token(token)[0])


# Playlist content CRUD
@app.task()
def show_playlist_content(playlist_id):
    return show_playlist_content(playlist_id)


@app.task()
def add_song_to_playlist(song_id, playlist_id, token):
    return add_song_to_playlist(song_id, playlist_id, user_info_from_session_token(token)[0])


@app.task()
def remove_song_from_playlist(song_id, playlist_id, token):
    return remove_song_from_playlist(song_id, playlist_id, user_info_from_session_token(token)[0])

@app.task()
def run_dump():
    return create_dump()


# Celery Test Code
@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y
# End of Celery Test Code
