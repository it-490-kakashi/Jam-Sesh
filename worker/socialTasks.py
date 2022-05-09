from creds import db
from models import liked_songs, song_list, news
from datetime import date
import sqlalchemy as sql
from sqlalchemy import update


def get_news_db():
    with db.connect() as conn:
        results = {}
        result = news.select().where(news.c.id != 0)
        results = conn.execute(result).fetchall()
        return results
