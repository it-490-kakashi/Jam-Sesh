"""
  Crud Blueprint for flask
"""
import os
import time
import dotenv
from flask import Blueprint, request
from .creds import celery_link

crud = Blueprint("crud", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()


def create_db():
    celery_link.send_task("tasks.create_db")


@crud.route("/add_test_user")
def add_test_user():
    first_name = "John"
    last_name = "Doe"
    user_task = celery_link.send_task("tasks.add_user", kwargs={"first": first_name, "last": last_name})
    return user_task.id


@crud.route("/add_user")
def add_user():
    user_task = celery_link.send_task("tasks.add_user", kwargs={"first_name": request.form["first_name"],
                                                                "last_name": request.form["last_name"],
                                                                "email": request.form["email"],
                                                                "username": request.form["username"],
                                                                "password": request.form["password"]})
    return user_task.id


@crud.route("/get_users")
def show_all_users():
    users_task = celery_link.send_task("tasks.get_users")
    while str(celery_link.AsyncResult(users_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    users_result = celery_link.AsyncResult(users_task.id).result
    return str(users_result)


@crud.route("/get_user")
def show_user():
    users_task = celery_link.send_task("tasks.get_user", kwargs={"user_id": request.form['user_id']})
    while str(celery_link.AsyncResult(users_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    users_result = celery_link.AsyncResult(users_task.id).result
    return users_result


@crud.route("/delete_user/<user_id>")
def delete_user(user_id):
    delete_task = celery_link.send_task("tasks.delete_user", kwargs={"user_id": user_id})
    while str(celery_link.AsyncResult(delete_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    delete_task_result = celery_link.AsyncResult(delete_task.id).result
    return str(delete_task_result)


# Figure out later
@crud.route("/update_user/", methods=["GET", "POST"])
def update_user():
    if request.method == "GET":
        return "Sorry this is not implemented yet"
    if request.method == "POST":
        update_task = celery_link.send_task("tasks.update_user",
                                            kwargs={"id": request.form["id"], "first": request.form["first_name"],
                                                    "last": request.form["last_name"]})
        update_task_result = celery_link.AsyncResult(update_task.id).result
        return str(update_task_result)


@crud.route("/test_likes")
def get_liked_songs():
    get_songs_task = celery_link.send_task("tasks.get_liked_songs", kwargs={"song_list": [1, 3, 5], "user_id": 3})
    while str(celery_link.AsyncResult(get_songs_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    get_songs_result = celery_link.AsyncResult(get_songs_task.id).result
    return str(get_songs_result)