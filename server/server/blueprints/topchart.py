import os
import time
import dotenv
import requests
from flask import Blueprint, request, render_template
from .creds import celery_link

dotenv.load_dotenv()

topten_charts = Blueprint("topcharts", __name__, static_folder=os.getenv("CURR_PATH")+"\static", template_folder=os.getenv("CURR_PATH")+"\templates")



@topten_charts.route('/topcharts', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        context = {
            'title': 'topcharts'
        }
        return render_template('topcharts.html', title=context['title'])

    if request.method == "POST":
        title = 'topcharts'
        results = []
        genius_results = request_loadtopcharts_audiodb().json()

        for song in genius_results['loved']:
            # song = song['result']
            result = {
                'strAlbumThumb': song['strAlbumThumb'],
                'strAlbum': song['strAlbum'],
                'strArtist': song['strArtist'],
                'strGenre': song['strGenre'],
                'intYearReleased': song['intYearReleased']
            }
            # result['song_profile'] = f"/song?id={result['song_id']}"
            results.append(result)
            # results = genius_results

    return render_template('topcharts.html', title=title, results=results)

def request_loadtopcharts_audiodb():
    url = "https://theaudiodb.p.rapidapi.com/mostloved.php"

    querystring = {"format":"album"}

    headers = {
        'x-rapidapi-host': "theaudiodb.p.rapidapi.com",
        'x-rapidapi-key': "5bcf48bf11msh7e2498cfa2449c0p1b31fejsn11fb62150ba6"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response