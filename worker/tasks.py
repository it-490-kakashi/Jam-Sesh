import time
import os
from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
from database.models import meta
import database.basic_crud as basic_crud
import utilities.find_user as find_user

load_dotenv()

logger = get_task_logger(__name__)

app = Celery('task',
             broker=os.getenv("BROKER_URL"),
             backend='db+postgresql+psycopg2://' + os.getenv("DATABASE_URL"))


# Creates tables
@app.task()
def create_db():
    meta.create_all()


# Create
@app.task()
def add_user(first_name, last_name, email, username, password):
    basic_crud.add_user(first_name, last_name, email, username, password)


# Read
@app.task()
def get_users():
    basic_crud.get_users()


# Read user @ id
@app.task()
def get_user(user_id):
    basic_crud.get_user(user_id)


# Update first/last @ id
@app.task()
def update_user(user_id, first, last):
    basic_crud.update_user(user_id, first, last)


# Delete
@app.task()
def delete_user(user_id):
    basic_crud.delete_user(user_id)


@app.task()
def login(username, password):
    #Code here
    return ""


@app.task()
def find_user_by(method, params):
    if type(params) is not list or tuple:
        return "ERROR: params is not a list or tuple"

    if method == "id":
        return find_user.by_id(params[0])
    if method == "username":
        return find_user.by_username(params[0])
    if method == "first&last":
        return find_user.by_first_and_last(params[0], params[1])

    return False


# Celery Test Code
@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y
# End of Celery Test Code
