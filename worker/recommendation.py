import json
import requests
import sys
from dotenv import load_dotenv
from creds import db
load_dotenv()


def get_recommended_songs(search_data):
    url = "https://shazam.p.rapidapi.com/songs/list-recommendations"

    querystring = {"key": search_data, "locale": "en-US"}

    headers = {
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
        "X-RapidAPI-Key": "23de317431msh3ab8b47dc37aca7p1e121ejsn95954c31b372"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data

'''
CLIENT_ID = "8e7fa19c9df7468ca923ada96fc35fd2"
CLIENT_SECRET = "8f3284d4854f4f7fbd5b384fe5d46ac1"
AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

def client_info():
    client_id = "8e7fa19c9df7468ca923ada96fc35fd2"
    secret_key = "8f3284d4854f4f7fbd5b384fe5d46ac1"
    spotify_token = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, secret_key))
    return spotify_token


def generate_label(text):
    return tk.Label(master= frm_recommendations,text=text)


def show_recommended_songs(response):
    with db.connect() as conn:
        display_track_name = tk.Label(master= frm_recommendations, text='Song Name')
        display_artist_name = tk.Label(master= frm_recommendations, text='Artist Name')
        display_play_it = tk.Label(master= frm_recommendations, text= 'Play')
        display_track_name.grid(row =0, column= 0)
        display_artist_name.grid(row= 0, column= 1)
        display_play_it.grid(row=0, column= 2)
        for index, track in enumerate(response['tracks']):
            display_track_name_recommended = generate_label(track['Name'])
            display_track_name_recommended.grid(row =index + 1, column= 0)
            display_artist_name_recommended = generate_label(track['Artists'][0]['Name'])
            display_artist_name_recommended.grid(row= index + 1, column= 1)


    
def get_recommended_songs(search_data):
    user_credentials = spotipy.Spotify(client_info())
    results = user_credentials.search(q=search_data, limit=1)
    id_list = [results['tracks']['items'][0]['id']]
    recommended = user_credentials.recommendations(seed_tracks=id_list, limit=20)
    return recommended

'''