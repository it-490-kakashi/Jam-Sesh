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
    if token_valid():
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
    return False


@playlist_interaction.route('/')
def show_playlist():
    context = {
        'title': 'User Playlists'
    }
    playlists = get_users_playlist()
    if playlists is False:
        return redirect('/login')

    # get playlist content
    return render_template('playlist.html', title=context['title'], playlists=playlists)


@playlist_interaction.route('/<int:id>')
def playlist_content(id):
    token = request.cookies.get('session_token')
    playlist_content = celery_link.send_task('tasks.show_playlist_content', kwargs={'playlist_id': id})
    while str(celery_link.AsyncResult(playlist_content.id).state) != "SUCCESS":
        time.sleep(0.25)
    playlist_content = celery_link.AsyncResult(playlist_content.id).result
    if len(playlist_content) == 0:
        redirect('/playlist')
    return render_template('playlist_content.html', playlist=playlist_content, title="User Playlist", playlist_id=id)


@playlist_interaction.route('/add', methods=['GET', 'POST'])
def playlist_add_song():
    token = request.cookies.get('session_token')
    if request.method == 'POST':
        playlist_id = request.form['playlist_id']
        add_song = celery_link.send_task('tasks.add_song_to_playlist',
                                         kwargs={'token': token, 'playlist_id': playlist_id,
                                                 'song_id': request.form['song_id']})
        while str(celery_link.AsyncResult(add_song.id).state) != "SUCCESS":
            time.sleep(0.25)
        add_song = celery_link.AsyncResult(add_song.id).result
        if add_song is False:
            return render_template('add_to_playlist.html', title="Add to Playlist", playlists=get_users_playlist(),
                                   message="Song ID not found")
        return redirect(f'/playlist/{playlist_id}')

    return render_template('add_to_playlist.html', title="Add to Playlist", playlists=get_users_playlist())


@playlist_interaction.route('/remove', methods=['POST'])
def playlist_remove_song():
    token = request.cookies.get('session_token')
    song_id = request.form['song_id']
    playlist_id = request.form['playlist_id']
    celery_link.send_task('tasks.remove_song_from_playlist',
                          kwargs={'song_id': song_id, 'playlist_id': playlist_id, 'token': token})

    return redirect(f'/playlist/{playlist_id}')


# Update
@playlist_interaction.route('/update/<int:id>', methods=['POST'])
def playlist_update_name(id):
    token = request.cookies.get('session_token')
    update_task = celery_link.send_task('tasks.update_playlist_name', kwargs={'token': token,
                                                                              'playlist_id': id,
                                                                              'new_name': request.form[
                                                                                  'playlist_name']})
    while str(celery_link.AsyncResult(update_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    update_result = celery_link.AsyncResult(update_task.id).result
    return redirect('/playlist')


# Delete
@playlist_interaction.route('/delete/<int:id>')
def playlist_delete(id):
    celery_link.send_task('tasks.delete_playlist', kwargs={'token': request.cookies.get('session_token'),
                                                           'playlist_id': id})
    return redirect('/playlist')
