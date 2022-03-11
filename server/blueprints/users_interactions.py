import os
import time
import dotenv
from flask import Blueprint, request, render_template, redirect
from .creds import celery_link

users_interactions = Blueprint("users_interactions", __name__, static_folder="../static",
                               template_folder="../templates")

dotenv.load_dotenv()


@users_interactions.route('/login', methods=["GET", "POST"])
def login():
    title = "login"
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form["username"]
        passwd = request.form["password"]
        login_request = celery_link.send_task("tasks.login", kwargs={'username': username, 'password': passwd})
        print("Sent Login Request")
        while str(celery_link.AsyncResult(login_request.id).state) != "SUCCESS":
            time.sleep(0.25)
        print("Login Processed")
        login_task_result = celery_link.AsyncResult(login_request.id).result
        if login_task_result:
            return redirect('/')  # Temporarily to home page but later account page
        return render_template('login.html', title=title, message="ERROR: Credentials incorrect")


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
        register_tasks = celery_link.send_task("tasks.register",
                           kwargs={'first_name': first,
                                   'last_name': last,
                                   'email': email,
                                   'username': usr,
                                   'password': password})

        while str(celery_link.AsyncResult(register_tasks.id).state) != "SUCCESS":
            time.sleep(0.25)
        register_result = celery_link.AsyncResult(register_tasks.id).result
        if register_result == True:
            return redirect('/login')
        else:
            return render_template('register.html', content="Email already in use!", first=first, last=last, username=usr, password=password, confirm=confirm)


@users_interactions.route('/account')
def account_page():
    return ""

