from creds import db
from models import liked_songs, song_list, news
from datetime import datetime
import sqlalchemy as sql
from sqlalchemy import update

def has_news():
    with db.connect() as conn:
        result = news.select().where(news.c.id!=0)
        result = conn.execute(result).fetchone()
        return result is not None

def seed_news():
    with db.connect() as conn:
        query = news.insert().values(Title="News", Body="Body", Author="Author", Published=datetime.now())
        conn.execute(query)
        query = news.insert().values(Title="News 2", Body="Body 2", Author="Author 2", Published=datetime.now())
        conn.execute(query)
        query = news.insert().values(Title="News 3", Body="Body 3", Author="Author 3", Published=datetime.now())
        conn.execute(query)
        query = news.insert().values(Title="News 4", Body="Body 4", Author="Author 4", Published=datetime.now())
        conn.execute(query)