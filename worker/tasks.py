import json
import time
import os
from celery import Celery
from celery.utils.log import get_task_logger
from celery.signals import worker_ready
from dotenv import load_dotenv
from models import create_all
import basic_crud as basic_crud
import find_user as find_user
import user_interactions as user_interactions
import song_interactions as song_interactions
from databaseseed import has_news, seed_news
from socialTasks import get_news_db

load_dotenv()

logger = get_task_logger(__name__)

app = Celery('task',
             broker=os.getenv("BROKER_URL"),
             backend='db+postgresql+psycopg2://' + os.getenv("DATABASE_URL"))


# Creates tables
@app.task()
def create_db():
    create_all()


# Create
@app.task()
def add_user(first_name, last_name, email, username, password):
    return basic_crud.add_user(first_name, last_name, email, username, password)


# Read
@app.task()
def get_users():
    return basic_crud.get_users()


# Read user @ id
@app.task()
def get_user(user_id):
    return basic_crud.get_user(user_id)


# Update first/last @ id
@app.task()
def update_user(user_id, first, last):
    return basic_crud.update_user(user_id, first, last)


# Delete
@app.task()
def delete_user(user_id):
    return basic_crud.delete_user(user_id)


@app.task()
def login(username, password):
    return user_interactions.login(username, password)


@app.task()
def register(username, first_name, last_name, email, password):
    return user_interactions.register(username, first_name, last_name, email, password)


@app.task()
def logout(session_token):
    return user_interactions.logout(session_token)


@app.task()
def token_valid(session_token):
    return user_interactions.user_session_valid(session_token)


@app.task()
def user_info_from_session_token(session_token):
    return user_interactions.user_info_from_session_token(session_token)


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


@app.task()
def get_liked_songs(song_list, user_id):
    return song_interactions.get_liked_songs(song_list, user_id)


@app.task()
def get_liked_song(song_id, user_id):
    return song_interactions.get_liked_song(song_id, user_id)


@app.task()
def like_song(genius_id, user_id):
    return song_interactions.like_song(genius_id, user_id)


@app.task()
def dislike_song(genius_id, user_id):
    return song_interactions.dislike_song(genius_id, user_id)


@app.task()
def add_song(name, artist, genre, genius_id):
    return song_interactions.add_song(name, artist, genre, genius_id)


@app.task()
def find_song(name, artist):
    return song_interactions.find_song(name, artist)

@app.task()
def update_views(genius_id):
    song_interactions.increaseView(genius_id)
    # to-do call increase views

@app.task()
def get_views(genius_id):
    return song_interactions.getView(genius_id)
    # Celery Test Code

@app.task()
def seed_if_empty():
    if not has_news():
        seed_news()

@app.task()
def get_news():
    return get_news_db()

@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y
# End of Celery Test Code
