import os
import time
import dotenv
from flask import Blueprint, request, render_template
from .creds import app_name

users_interactions = Blueprint("users_interactions", __name__, static_folder="../static",
                               template_folder="../templates")

dotenv.load_dotenv()


@users_interactions.route('/', methods=["GET", "POST"])
@users_interactions.route('/login', methods=["GET", "POST"])
def index():
    title = "login"
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form["username"]
        passwd = request.form["password"]
        login_request = app_name.send_task("tasks.login", kwargs={'username': username, 'password': passwd})
        print("Sent Login Request")
        while str(app_name.AsyncResult(login_request.id).state) != "SUCCESS":
            time.sleep(0.25)
        print("Login Processed")
        login_task_result = app_name.AsyncResult(login_request.id).result
        if login_task_result:
            return render_template('display.html', content="Login Successful")
        return render_template('login.html', title=title, message="ERROR: User not found")


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
        app_name.send_task("tasks.add_user",
                           kwargs={'first_name': first,
                                   'last_name': last,
                                   'email': email,
                                   'username': usr,
                                   'password': password})
        #TODO: Update page if email is in use
        return render_template('display.html', content=email, content2=usr, content3=password, content4=confirm)
