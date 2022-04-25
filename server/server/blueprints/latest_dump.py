import os
import time
import dotenv
from flask import Blueprint, render_template
from .creds import celery_link

dotenv.load_dotenv()

user_dump = Blueprint("user_dump", __name__, static_folder=os.getenv("CURR_PATH")+"\static", template_folder=os.getenv("CURR_PATH")+"\templates")



@user_dump.route('/user_dump')
def users_show():
    title = "user dump"
    users = celery_link.send_task("tasks.get_latest_dump")
    while str(celery_link.AsyncResult(users.id).state) != "SUCCESS":
        time.sleep(0.1)
    users = celery_link.AsyncResult(users.id).result
    return render_template('latest_dump.html', title=title, users=users)
