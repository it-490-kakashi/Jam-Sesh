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
                  Column('genre', String)
                  )

liked_songs = Table('liked_songs', meta,
                    Column('id', Integer, Identity('liked_song_id_seq', start=1, increment=1), primary_key=True),
                    Column('song_id', None, ForeignKey('songs.id')),
                    Column('user_id', None, ForeignKey('users.id'))
                    )
