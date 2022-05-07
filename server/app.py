from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
from blueprints.crud import crud, create_db
from blueprints.celery_test import celery_test
from blueprints.song_search import song_search
from blueprints.users import users
from blueprints.users_interactions import users_interactions
from blueprints.song_interaction import song_interaction
from blueprints.playlist_interaction import playlist_interaction
from blueprints.topchart import topten_charts
from blueprints.topsong import top_songs
from blueprints.creds import celery_link
import time
import requests
load_dotenv()

app = Flask(__name__)
app.register_blueprint(crud, url_prefix='/api')
app.register_blueprint(celery_test, url_prefix='/celery')
app.register_blueprint(song_search, url_prefix='')
app.register_blueprint(users, url_prefix='')
app.register_blueprint(users_interactions)
app.register_blueprint(song_interaction, url_prefix='')
app.register_blueprint(playlist_interaction, url_prefix='/playlist')
app.register_blueprint(topten_charts, url_prefix='')
app.register_blueprint(top_songs, url_prefix='')


@app.before_first_request
def make_db():
    create_db()


@app.route('/')
def hello_world():

    title = 'Home Page'

    news_elements = fetch_news()
    return render_template('home.html', title=title, news=news_elements)

def fetch_news():

    url = "https://bing-news-search1.p.rapidapi.com/news"

    querystring = {"category": "Entertainment_Music", "safeSearch": "Off", "textFormat": "Raw"}

    headers = {
        "X-BingApis-SDK": "true",
        "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com",
        "X-RapidAPI-Key": "5bcf48bf11msh7e2498cfa2449c0p1b31fejsn11fb62150ba6"
    }
    results = []
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    for article in response['value']:
        result = {
            'Title': article['name'],
            'Body': article['description'],
            'Published': article['datePublished'],
            'Author': article['url'],
            'Image': article['image']['thumbnail']['contentUrl']
        }
        results.append(result)
    return results


@app.route('/search')
def hello_search():
    context = {
        'title': 'Search Page'
    }
    return render_template('search.html', data=context)

@app.route('/register')
def hello_register():
    context = {
        'title': 'Register Page'
    }
    return render_template('register.html.html', data=context)

@app.route('/login')
def hello_login():
    context = {
        'title': 'Login Page'
    }
    return render_template('login.html', data=context)


if __name__ == '__main__':
    app.run()
