import os
import time
import dotenv
from flask import Blueprint, render_template
from .creds import celery_link
from .crud import show_all_users

users = Blueprint("users", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()


@users.route('/show_users')
def show_users():
    title = "All Users"

    return render_template('user_list.html', title=title, users=show_all_users())

