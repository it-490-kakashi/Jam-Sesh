import os
import time
import dotenv
import requests
from flask import Blueprint, request, render_template
from celery import Celery

api_calls = Blueprint("api_calls", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()

app_name = Celery("task", broker=os.getenv("BROKER_URL"),
                  backend="db+postgresql+psycopg2://" + os.getenv("DATABASE_URL"))


@api_calls.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        context = {
            'title': 'Search'
        }
        return render_template('search.html', title=context['title'])

    if request.method == "POST":
        title = 'Search'
        results = []
        spotify_results = request_song_info_spotify(request.form['search_info']).json()
        for song in spotify_results['tracks']['items']:
            song = song['data']
            result = {
                'spotify_id': song['id'],
                'name': song['name'],
                'album': song['albumOfTrack']['name'],
                'artist': song['artists']['items'][0]['profile']['name'],
            }
            audiodb_result = request_song_info_audiodb(result['artist'], result['name']).json()
            if audiodb_result['track'] is not None:
                result['music_video'] = audiodb_result['track'][0]['strMusicVid']
                result['audiodb_id']
            results.append(result)

        #return context['results']
        return render_template('search.html', title=title, results=results, placeholder=request.form['search_info'])


def request_song_info_genius(search_info):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + os.getenv('GENIUS_AUTH')}
    search_url = base_url + '/search'
    data = {'q': search_info}
    response = requests.get(search_url, data=data, headers=headers)

    return response


def request_song_info_spotify(search_info):
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q": search_info, "type": "tracks" , "limit":15}

    headers = {
        'x-rapidapi-host': "spotify23.p.rapidapi.com",
        'x-rapidapi-key': "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }
    response = requests.get(url, headers=headers, params=querystring)

    return response


def request_song_info_audiodb(artist, track_name):
    url = "https://theaudiodb.p.rapidapi.com/searchtrack.php"

    querystring = {"s": artist, "t": track_name}

    headers = {
        'x-rapidapi-host': "theaudiodb.p.rapidapi.com",
        'x-rapidapi-key': "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response


def request_song_by_id_spotify(song_id):
    url = "https://spotify23.p.rapidapi.com/tracks/"
    if type(song_id) == "string":
        querystring = {"ids": song_id}
    else:
        querystring = {"ids": ','.join(song_id)}

    headers = {
        'x-rapidapi-host': "spotify23.p.rapidapi.com",
        'x-rapidapi-key': "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }

    response = requests.get( url, headers=headers, params=querystring)

    return response