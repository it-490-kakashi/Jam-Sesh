"""
  Crud Blueprint for flask
"""
import json
import os
import time
import dotenv
from flask import Blueprint, request
from .creds import celery_link
import requests
import hashlib

crud = Blueprint("crud", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()


def create_db():
    databasestatus = celery_link.send_task("tasks.create_db")
    while str(celery_link.AsyncResult(databasestatus.id).state) != "SUCCESS":
        time.sleep(0.1)


@crud.route("/add_test_news")
def add_test_news():
    news_task = celery_link.send_task("tasks.seed_if_empty")
    return news_task.id


@crud.route("/add_test_user")
def add_test_user():
    url = "https://my.api.mockaroo.com/it490___users.json"

    payload = {}
    headers = {
        'X-API-Key': '3f00bd30',
        'Content-Type': 'application/json',
        'Cookie': 'layer0_bucket=14; layer0_destination=default; layer0_environment_id_info=1680b086-a116-4dc7-a17d-9e6fdbb9f6d9'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    test_users = json.loads(response.text)

    user_task_ids = []
    for user in test_users:
        hash_input = hashlib.sha256(user['password'].encode())
        hashword = hash_input
        user_task = celery_link.send_task("tasks.add_user", kwargs={"first_name": user['first_name'],
                                                                    "last_name": user['last_name'],
                                                                    "email": user['email'],
                                                                    "username": user['username'],
                                                                    "password": user['password'],
                                                                    "hashed password": hashword})
        user_task_ids.append(user_task.id)
    return str(user_task_ids)


@crud.route("/add_user")
def add_user():
    hash_input = hashlib.sha256(request.form["password"].encode())
    hashword = hash_input
    user_task = celery_link.send_task("tasks.add_user", kwargs={"first_name": request.form["first_name"],
                                                                "last_name": request.form["last_name"],
                                                                "email": request.form["email"],
                                                                "username": request.form["username"],
                                                                "password": request.form["password"],
                                                                "hashed": hashword})
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
