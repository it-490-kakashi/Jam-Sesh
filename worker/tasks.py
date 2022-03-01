import time
import os
from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
from database import db, meta, basic_user, song_list, liked_songs
from sqlalchemy import exc

load_dotenv()

logger = get_task_logger(__name__)

app = Celery('task',
             broker=os.getenv("BROKER_URL"),
             backend='db+postgresql+psycopg2://' + os.getenv("DATABASE_URL"))


@app.task()
def create_db():
    meta.create_all()


# TODO: REFRACTOR CODE TO FOLLOW ARTICLE https://www.askpython.com/python-modules/flask/flask-crud-application

# Create
@app.task()
def add_user(first, last):
    with db.connect() as conn:
        try:
            new_user = basic_user.insert().values(first_name=first, last_name=last)
            conn.execute(new_user)
            return "User Added"
        except exc.SQLAlchemyError:
            return "ERROR: " + str(exc.SQLAlchemyError)


# Read
@app.task()
def get_users():
    with db.connect() as conn:
        try:
            select = basic_user.select()
            result = conn.execute(select)
            return result.fetchall()
        except exc.SQLAlchemyError as e:
            return "ERROR: " + str(e)


# Read certain user
@app.task()
def get_user(user_id):
    with db.connect() as conn:
        try:
            select = basic_user.select().where(basic_user.c.id == user_id)
            return conn.execute(select).fetchall()
        except exc.SQLAlchemyError as e:
            return "ERROR: " + str(e)


# Update
@app.task()
def update_user(user_id, first, last):
    with db.connect() as conn:
        try:
            update = basic_user.update().where(basic_user.c.id == user_id).values(first=first, last=last)
            conn.execute(update)
        except exc.SQLAlchemyError:
            return "ERROR: " + str(exc.SQLAlchemyError)


# Delete
@app.task()
def delete_user(user_id):
    with db.connect() as conn:
        try:
            user = basic_user.select().where(basic_user.c.id == user_id)
            result = conn.execute(user)
            if len(result.fetchall()) == 0:
                return f"ERROR: User @ id:{user_id} is not found "

            conn.execute(basic_user.delete().where(basic_user.c.id == user_id))
            return f"Deleted user @ id:{user_id}"
        except exc.NoResultFound:
            return "ERROR: " + str(exc.SQLAlchemyError)


# Celery Test Code
@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y
# End of Celery Test Code
