import json
import os
import sys
import time
import dotenv
import requests
from flask import Blueprint, request, render_template, redirect, make_response
from .creds import celery_link

recommendation = Blueprint("recommendation", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()


@recommendation.route('/recommendation', methods=['GET', 'POST'])
def recommend_song():
    if request.method == "GET":
        context = {
            'title': 'Search'
        }
        return render_template('recommended_result.html', title=context['title'])

    if request.method == "POST":
        title = "Search"
        shazam_results = request_song_info_shazam(request.form['search_info'])
        search = shazam_results

        songs_found = celery_link.send_task("tasks.get_recommended", kwargs={"search": search})

        while str(celery_link.AsyncResult(songs_found.id).state) != "SUCCESS":
            time.sleep(0.1)

        results = json.loads(celery_link.AsyncResult(songs_found.id).result)

    return render_template('recommended_result.html', title=title, results=results, placeholder=request.form['search_info'])

def request_song_info_shazam(info):
    url = "https://shazam.p.rapidapi.com/search"

    querystring = {"term": info, "locale": "en-US", "offset": "0", "limit": "1"}

    headers = {
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
        "X-RapidAPI-Key": "23de317431msh3ab8b47dc37aca7p1e121ejsn95954c31b372"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    key = data['tracks']['hits']
    for k in key:
        val = k['track']['key']

    return val
'''
def request_song_info_spotify(info):
    url = "https://api.spotify.com/v1/recommendations"
    client_id = "8e7fa19c9df7468ca923ada96fc35fd2"
    secret_key = "8f3284d4854f4f7fbd5b384fe5d46ac1"
    # track/6wQlQrTY5mVS8EGaFZVwVF
    querystring = {"q": info, "type": "track", "limit": 15}

    headers = {
        'client_id': client_id,
        'secret_key': secret_key,
    }
    response = requests.get(url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    print(json_data, file=sys.stderr)
    return json_data

'''