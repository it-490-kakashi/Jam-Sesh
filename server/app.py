from flask import Flask, redirect, render_template, request
import os
import requests
from dotenv import load_dotenv
from blueprints.crud import crud
from blueprints.celery_test import celery_test

load_dotenv()

app = Flask(__name__)
app.register_blueprint(crud, url_prefix="/api")
app.register_blueprint(celery_test, url_prefix="/celery")


@app.before_first_request
def create_db():
    return redirect('/api/create_db')


@app.route('/')
def hello_world():
    context = {
        'title': 'Home Page'
    }
    return render_template('base.html', data=context)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        context = {
            'title': 'Search'
        }
        return render_template('search.html', title=context['title'])

    if request.method == "POST":
        context = {
            'title': 'Search',
            'results': request_song_info(request.form['search_info']).json(),
        }
        return render_template('search.html', title=context['title'], results=context['results'])


def request_song_info(search_info):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + os.getenv('GENIUS_AUTH')}
    search_url = base_url + '/search'
    data = {'q': search_info}
    response = requests.get(search_url, data=data, headers=headers)

    return response

if __name__ == '__main__':
    app.run()
