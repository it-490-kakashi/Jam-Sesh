from flask import Blueprint, request, redirect
import dotenv
from .creds import celery_link
import time

dotenv.load_dotenv()

song_interaction = Blueprint('song_interaction', __name__, static_folder="../static", template_folder="../templates")


def get_liked_song(genius_id, user_id):
    get_songs_task = celery_link.send_task("tasks.get_liked_song", kwargs={"song_id": genius_id, "user_id": user_id})
    while str(celery_link.AsyncResult(get_songs_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    get_songs_result = celery_link.AsyncResult(get_songs_task.id).result
    return str(get_songs_result)


@song_interaction.route('/like_song')
def like_song():
    genius_id = int(request.args['genius_id'])
    user_id = int(request.args['user_id'])
    if get_liked_song(genius_id, user_id) == "False":
        task = celery_link.send_task("tasks.like_song", kwargs={"genius_id":genius_id, "user_id":user_id})
        while str(celery_link.AsyncResult(task.id).state) != "SUCCESS":
            time.sleep(0.25)
    return redirect(f'/song?id={genius_id}')


@song_interaction.route('/dislike_song')
def dislike_song():
    genius_id = int(request.args['genius_id'])
    user_id = int(request.args['user_id'])
    if get_liked_song(genius_id, user_id) == "True":
        task = celery_link.send_task("tasks.dislike_song", kwargs={"genius_id":genius_id, "user_id":user_id})
        while str(celery_link.AsyncResult(task.id).state) != "SUCCESS":
            time.sleep(0.25)
    return redirect(f'/song?id={genius_id}')