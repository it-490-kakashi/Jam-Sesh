from flask import Flask, redirect, render_template, request
import os
import requests
from dotenv import load_dotenv
from blueprints.crud import crud
from blueprints.celery_test import celery_test
from blueprints.api_calls import api_calls

load_dotenv()

app = Flask(__name__)
app.register_blueprint(crud, url_prefix="/api")
app.register_blueprint(celery_test, url_prefix="/celery")
app.register_blueprint(api_calls, url_prefix="")


@app.before_first_request
def create_db():
    return redirect('/api/create_db')


@app.route('/')
def hello_world():
    context = {
        'title': 'Home Page'
    }
    return render_template('base.html', data=context)





if __name__ == '__main__':
    app.run()
