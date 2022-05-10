import os
import time
import dotenv
from flask import Blueprint, request, render_template, redirect, make_response
from .creds import celery_link

users_interactions = Blueprint("users_interactions", __name__, static_folder="../static",
                               template_folder="../templates")

dotenv.load_dotenv()


@users_interactions.route('/login', methods=["GET", "POST"])
def login():
    title = "login"
    if token_valid() is False:
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            username = request.form["username"]
            passwd = request.form["password"]
            login_request = celery_link.send_task("tasks.login", kwargs={'username': username, 'password': passwd})
            while str(celery_link.AsyncResult(login_request.id).state) != "SUCCESS":
                time.sleep(0.25)
            login_task_result = celery_link.AsyncResult(login_request.id).result
            if login_task_result is None:
                return render_template('login.html', title=title, message="ERROR: Credentials incorrect")
            if login_task_result[0]:
                if request.cookies.get('session_token') is None:
                    resp = make_response(redirect('/account'))
                    resp.set_cookie(key='session_token', value=login_task_result[1])
                    return resp
                return redirect('/account')
    return redirect('/account')


@users_interactions.route('/register', methods=["GET", "POST"])
def register():
    if not token_valid():
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
            if register_result:
                return redirect('/login')
            else:
                return render_template('register.html', message="Email already in use!", first=first, last=last, username=usr, password=password, confirm=confirm)
    return redirect('/account')


@users_interactions.route('/logout')
def logout():
    # Get session token
    session_token = request.cookies.get('session_token')
    # if token set
    if token_valid():
        logout_task = celery_link.send_task('tasks.logout', kwargs={'session_token': session_token})
        while str(celery_link.AsyncResult(logout_task.id).state) != "SUCCESS":
            time.sleep(0.25)
        register_result = celery_link.AsyncResult(logout_task.id).result
        if register_result:
            resp = make_response(redirect('/login'))
            resp.set_cookie('session_token', '', expires=0)
            return resp
        # Log out user
        # Redirect to home
    return redirect('/login')
    # redirect login


@users_interactions.route('/account')
def account_page():
    # Get session token
    session_token = request.cookies.get('session_token')
    if not token_valid():
        return redirect('/login')
    session_valid = celery_link.send_task('tasks.token_valid', kwargs={'session_token':session_token})
    while str(celery_link.AsyncResult(session_valid.id).state) != "SUCCESS":
        time.sleep(0.25)
    session_valid = celery_link.AsyncResult(session_valid.id).result
    # if token valid
    if session_valid:
        # Send token to backend asking for user information
        account_info = celery_link.send_task('tasks.user_info_from_session_token', kwargs={'session_token':session_token})
        while str(celery_link.AsyncResult(account_info.id).state) != "SUCCESS":
            time.sleep(0.25)
        # Get user info from backend
        account_info = celery_link.AsyncResult(account_info.id).result
        account_info = {
            "first_name": account_info[1],
            "last_name": account_info[2],
            "email": account_info[3],
            "username": account_info[4]
        }
        # Display user info on frontend
        return render_template('account_profile.html', account=account_info)
    return redirect('/login')


def token_valid():
    session_token = request.cookies.get('session_token')
    if session_token is not None:
        session_valid_task = celery_link.send_task('tasks.token_valid', kwargs={'session_token':session_token})
        while str(celery_link.AsyncResult(session_valid_task.id).state) != "SUCCESS":
            time.sleep(0.25)
        return celery_link.AsyncResult(session_valid_task.id).result
    return False

