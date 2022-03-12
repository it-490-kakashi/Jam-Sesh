from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
from blueprints.crud import crud, create_db
from blueprints.celery_test import celery_test
from blueprints.song_search import song_search
from blueprints.users import users
from blueprints.users_interactions import users_interactions
from blueprints.song_interaction import song_interaction


load_dotenv()

app = Flask(__name__)
app.register_blueprint(crud, url_prefix='/api')
app.register_blueprint(celery_test, url_prefix='/celery')
app.register_blueprint(song_search, url_prefix='')
app.register_blueprint(users, url_prefix='')
app.register_blueprint(users_interactions)
app.register_blueprint(song_interaction, url_prefix='')



@app.before_first_request
def make_db():
    create_db()


@app.route('/')
def hello_world():
    context = {
        'title': 'Home Page'
    }
    return render_template('base.html', data=context)


if __name__ == '__main__':
    app.run()
