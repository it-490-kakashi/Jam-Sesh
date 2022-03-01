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
        genius_results = request_song_info_genius(request.form['search_info']).json()
        for song in genius_results['response']['hits']:
            song = song['result']
            result = {
                'song_id': song['id'],
                'name': song['title'],
                'artist': song['artist_names'],
            }
            result['song_profile'] = f"/song?id={result['song_id']}"
            results.append(result)

        #return context['results']
        return render_template('search.html', title=title, results=results, placeholder=request.form['search_info'])


@api_calls.route('/song', methods=['GET', 'POST'])
def song_profile():
    from urllib import parse

    title = "Song Profile Page"
    if request.args is not None:
        result = request_song_id_genius(request.args['id']).json()
        result = result['response']['song']
        for media in result['media']:
            if media['provider'] == "youtube":
                url = media['url']
                query_def = parse.parse_qs(parse.urlparse(url).query)['v'][0]
                result['youtube_id'] = query_def
        title = result['full_title']

    return render_template('song_profile.html', title=title, result=result)


# API CALLS

def request_song_info_genius(search_info):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + os.getenv('GENIUS_AUTH')}
    search_url = base_url + '/search'
    data = {'q': search_info}
    response = requests.get(search_url, data=data, headers=headers)

    return response


def request_song_id_genius(song_id):
    url = "https://genius.p.rapidapi.com/songs/"+song_id

    headers = {
        'x-rapidapi-host': "genius.p.rapidapi.com",
        'x-rapidapi-key': "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }

    response = requests.request("GET", url, headers=headers)

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