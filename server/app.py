from flask import Flask, redirect
import os
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
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
