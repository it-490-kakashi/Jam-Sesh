import os
import time
import dotenv
from flask import Blueprint, request, render_template
from .creds import app_name

users_interactions = Blueprint("users_interactions", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()

@users_interactions.route('/', methods=["GET", "POST"])
@users_interactions.route('/login', methods=["GET", "POST"])
def index():  # put application's code here
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form["username"]
        passwd = request.form["password"]
        if find_user(username=username, password=passwd):
            return render_template('display.html', content="Login Successful")

        return "Error: Invalid Information!"


@users_interactions.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        first = request.form["first"]
        last = request.form["last"]
        email = request.form["email"]
        usr = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        add_user(first=first, last=last, email=email, username=usr, password=password)
        return render_template('display.html', content=email, content2=usr, content3=password, content4=confirm)
