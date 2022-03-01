import os
import dotenv
from flask import Blueprint, render_template
from server.creds.creds import app_name

dotenv.load_dotenv()

celery_test = Blueprint("celery_test", __name__, static_folder="../static", template_folder="../templates")


# Celery Test Code
@celery_test.route('/simple_start_task', methods=["POST"])
def call_method():
    print("Invoking Method ")
    r = app_name.send_task('tasks.longtime_add', kwargs={'x': 1, 'y': 2})
    print(r.backend)
    return r.id


@celery_test.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = app_name.AsyncResult(task_id, app=app_name)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@celery_test.route('/simple_task_result/<task_id>')
def task_result(task_id):
    result = app_name.AsyncResult(task_id).result
    return "Result of the Task " + str(result)

# End of Celery Test Code
