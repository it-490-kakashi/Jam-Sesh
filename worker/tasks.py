import time
import os
from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
from sqlalchemy import create_engine, exc
from sqlalchemy import Table, Column, String, MetaData, Integer, Identity, ForeignKey

load_dotenv()

logger = get_task_logger(__name__)

app = Celery('task',
             broker=os.getenv("BROKER_URL"),
             backend='db+postgresql+psycopg2://' + os.getenv("DATABASE_URL"))

db = create_engine("postgresql://" + os.getenv("DATABASE_URL"))

# SQL Expression Language
meta = MetaData(db)
basic_user = Table('users', meta,
                   Column('id', Integer, Identity(start=1, cycle=True), primary_key=True),
                   Column('first_name', String),
                   Column('last_name', String),
                   Column('email', String),
                   Column('username', String),
                   Column('password', String)
                   )

song_list = Table('songs', meta,
                  Column('id', Integer, Identity(start=1, cycle=True), primary_key=True),
                  Column('name', String),
                  Column('artist', String),
                  Column('genre', String)
                  )

liked_songs = Table('liked_songs', meta,
                    Column('id', Integer, Identity(start=1, cycle=True), primary_key=True),
                    Column('song_id', None, ForeignKey('songs.id')),
                    Column('user_id', None, ForeignKey('users.id'))
                    )


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
            conn.execute(basic_user.select().where(basic_user.c.id == user_id))

            delete = basic_user.delete().where(basic_user.c.id == user_id)
            conn.execute(delete)
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
