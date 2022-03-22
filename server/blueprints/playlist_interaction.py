from flask import Blueprint, request, redirect, render_template
import dotenv
from .creds import celery_link
import time
from .users_interactions import token_valid

dotenv.load_dotenv()

playlist_interaction = Blueprint('playlist_interaction', __name__, static_folder="../static",
                                 template_folder="../templates")


# Playlist CRUD

# Create
@playlist_interaction.route('/create', methods=['GET', 'POST'])
def create_playlist():
    if token_valid():
        if request.method == 'POST':
            name = request.form['playlist_name']
            token = request.cookies.get('session_token')
            celery_link.send_task("tasks.new_playlist", kwargs={'name': name, 'token': token})

            return redirect('/account')

        return render_template('create_playlist.html', title="Create Playlist")
    return redirect('/login')


# Read
@playlist_interaction.route('/')
def show_playlist():
    context = {
        'title': 'User Playlists'
    }
    token = request.cookies.get('session_token')
    playlist_list = celery_link.send_task('tasks.get_user_playlists', kwargs={'token': token})
    while str(celery_link.AsyncResult(playlist_list.id).state) != "SUCCESS":
        time.sleep(0.25)
    playlist_list = celery_link.AsyncResult(playlist_list.id).result
    new_list = []
    for item in playlist_list:
        new_elm = {
            'id': item[0],
            'name': item[2]
        }
        new_list.append(new_elm)
    playlist_list = new_list
    # get playlist content
    return render_template('playlist.html', title=context['title'], playlists=playlist_list)

# Update


# Delete
