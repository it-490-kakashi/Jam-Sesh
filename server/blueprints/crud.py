"""
  Crud Blueprint for flask
"""
import json
import os
import time
import dotenv
from flask import Blueprint, request
from .creds import app_name

crud = Blueprint("crud", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()


def create_db():
    app_name.send_task("tasks.create_db")


@crud.route("/add_test_user")
def add_test_user():
    first_name = "John"
    last_name = "Doe"
    user_task = app_name.send_task("tasks.add_user", kwargs={"first": first_name, "last": last_name})
    return user_task.id


@crud.route("/add_user")
def add_user():
    user_task = app_name.send_task("tasks.add_user", kwargs={"first": request.form["first_name"],
                                                             "last": request.form["last_name"]})
    return user_task.id


@crud.route("/get_users")
def show_all_users():
    users_task = app_name.send_task("tasks.get_users")
    while str(app_name.AsyncResult(users_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    users_result = app_name.AsyncResult(users_task.id).result
    return users_result


@crud.route("/get_user")
def show_user():
    users_task = app_name.send_task("tasks.get_user", kwargs={"user_id": request.form['user_id']})
    while str(app_name.AsyncResult(users_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    users_result = app_name.AsyncResult(users_task.id).result
    return users_result


@crud.route("/delete_user/<user_id>")
def delete_user(user_id):
    delete_task = app_name.send_task("tasks.delete_user", kwargs={"user_id": user_id})
    while str(app_name.AsyncResult(delete_task.id).state) != "SUCCESS":
        time.sleep(0.25)
    delete_task_result = app_name.AsyncResult(delete_task.id).result
    return str(delete_task_result)


# Figure out later
@crud.route("/update_user/", methods=["GET", "POST"])
def update_user():
    if request.method == "GET":
        return "Sorry this is not implemented yet"
    if request.method == "POST":
        update_task = app_name.send_task("tasks.update_user",
                                         kwargs={"id": request.form["id"], "first": request.form["first_name"],
                                                 "last": request.form["last_name"]})
        update_task_result = app_name.AsyncResult(update_task.id).result
        return str(update_task_result)
