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

            return redirect('/playlist')

        return render_template('create_playlist.html', title="Create Playlist")
    return redirect('/login')


# Read
def get_users_playlist():
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
    return new_list


@playlist_interaction.route('/')
def show_playlist():
    context = {
        'title': 'User Playlists'
    }

    # get playlist content
    return render_template('playlist.html', title=context['title'], playlists=get_users_playlist())


@playlist_interaction.route('/<int:id>')
def playlist_content(id):
    token = request.cookies.get('session_token')
    playlist_content = celery_link.send_task('tasks.get_user_playlist', kwargs={'token': token, 'playlist_id': id})
    while str(celery_link.AsyncResult(playlist_content.id).state) != "SUCCESS":
        time.sleep(0.25)
    playlist_content = celery_link.AsyncResult(playlist_content.id).result
    if len(playlist_content) == 0:
        redirect('/playlist')
    return render_template('playlist_content.html', playlist=playlist_content, title="User Playlist")


@playlist_interaction.route('/add', methods=['GET', 'POST'])
def playlist_add_song():
    token = request.cookies.get('session_token')
    if request.method == 'POST':
        playlist_id = request.form['playlist_id']
        celery_link.send_task('tasks.add_song_to_playlist',
                              kwargs={'token': token, 'playlist_id': playlist_id,
                                      'song_id': request.form['song_id']})
        return redirect(f'/playlist/{playlist_id}')

    return render_template('add_to_playlist.html', title="Add to Playlist", playlists=get_users_playlist())

# Update


# Delete
