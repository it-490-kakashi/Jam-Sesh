import os
import time
import dotenv
import requests
from flask import Blueprint, request, render_template
from .creds import celery_link

top_songs = Blueprint("topsongs", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()


@top_songs.route('/topsongs', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        context = {
            'title': 'topsongs'
        }
        return render_template('topsongs.html', title=context['title'])

    if request.method == "POST":
        title = 'topsongs'
        results = []
        genius_results = request_loadtopsongs_audiodb().json()

        for song in genius_results['loved']:
            # song = song['result']
            if song['strGenre'] == request.form['genre'] or request.form['genre'] == "All":
                result = {
                    'strAlbum': song['strAlbum'],
                    'strArtist': song['strArtist'],
                    'strGenre': song['strGenre'],
                    'strTrack': song['strTrack'],
                    'intTotalPlays': song['intTotalPlays']
                }
                # result['song_profile'] = f"/song?id={result['song_id']}"
                results.append(result)
                # results = genius_results

    return render_template('topsongs.html', title=title, results=results)

def request_loadtopsongs_audiodb():
    url = "https://theaudiodb.p.rapidapi.com/mostloved.php"

    querystring = {"format":"track"}

    headers = {
        'x-rapidapi-host': "theaudiodb.p.rapidapi.com",
        'x-rapidapi-key': "5bcf48bf11msh7e2498cfa2449c0p1b31fejsn11fb62150ba6"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response