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
@playlist_interaction.route('/read/<int:id>')
def show_playlist(id):
    context = {
        'title': 'playlist_name'
    }
    # get playlist content
    return render_template('playlist.html', title=context['title'])

# Update


# Delete
