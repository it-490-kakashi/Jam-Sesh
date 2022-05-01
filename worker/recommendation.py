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
