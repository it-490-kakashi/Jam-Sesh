from flask import Flask, redirect, render_template, request
import os
import requests
from dotenv import load_dotenv
from blueprints.crud import crud, create_db
from blueprints.celery_test import celery_test
from blueprints.api_calls import api_calls
from blueprints.users_interactions import users_interactions

load_dotenv()

app = Flask(__name__)
app.register_blueprint(crud, url_prefix="/api")
app.register_blueprint(celery_test, url_prefix="/celery")
app.register_blueprint(api_calls, url_prefix="")
app.register_blueprint(users_interactions, url_prefix="")


@app.before_first_request
def make_db():
    create_db()


@app.route('/base')
def hello_world():
    context = {
        'title': 'Home Page'
    }
    return render_template('base.html', data=context)


if __name__ == '__main__':
    app.run()
