from creds import db
from sqlalchemy import Table, Column, String, MetaData, Integer, Identity, ForeignKey, DateTime, func

# SQL Expression Language
meta = MetaData(db)
basic_user = Table('users', meta,
                   Column('id', Integer, Identity('user_id_seq', start=1, increment=1), primary_key=True),
                   Column('first_name', String),
                   Column('last_name', String),
                   Column('email', String),
                   Column('username', String),
                   Column('password', String),
                   Column('hashed', String),
                   Column('last_login', DateTime)
                   )

logged_in_user = Table('logged_in_users', meta,
                       Column('user_id', None, ForeignKey('users.id')),
                       Column('session_token', String),
                       Column('token_expiry', DateTime)
                       )

song_list = Table('songs', meta,
                  Column('id', Integer, Identity('song_id_seq', start=1, increment=1), primary_key=True),
                  Column('name', String),
                  Column('artist', String),
                  Column('genre', String),
                  Column('genius_id', Integer, primary_key=True, unique=True),
                  Column('views', Integer)
                  )

liked_songs = Table('liked_songs', meta,
                    Column('id', Integer, Identity('liked_song_id_seq', start=1, increment=1), primary_key=True),
                    Column('song_id', None, ForeignKey('songs.genius_id')),
                    Column('user_id', None, ForeignKey('users.id'))
                    )

playlist = Table('playlists', meta,
                 Column('id', Integer, Identity('playlist_id_seq', start=1, increment=1), primary_key=True),
                 Column('user_id', None, ForeignKey('users.id')),
                 Column('playlist_name', String)
                 )

playlist_content = Table('playlist_content', meta,
                         Column('playlist_id', None, ForeignKey('playlists.id')),
                         Column('song_id', None, ForeignKey('songs.genius_id'))
                         )
news = Table('news_table', meta,
             Column('id', Integer, Identity('news_id_seq', start=1, increment=1), primary_key=True),
             Column('Title', String),
             Column('Body', String),
             Column('Author', String),
             Column('Published', DateTime)
             )


def create_all():
    meta.create_all()
