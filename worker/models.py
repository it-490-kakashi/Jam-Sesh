from creds import db
from sqlalchemy import Table, Column, String, MetaData, Integer, Identity, ForeignKey, Sequence


# SQL Expression Language
meta = MetaData(db)
basic_user = Table('users', meta,
                   Column('id', Integer, Identity('user_id_seq', start=1, increment=1), primary_key=True),
                   Column('first_name', String),
                   Column('last_name', String),
                   Column('email', String),
                   Column('username', String),
                   Column('password', String)
                   )

song_list = Table('songs', meta,
                  Column('id', Integer, Identity('song_id_seq', start=1, increment=1), primary_key=True),
                  Column('name', String),
                  Column('artist', String),
                  Column('genre', String),
                  Column('genius_id', Integer, primary_key=True, unique=True),
                  )

liked_songs = Table('liked_songs', meta,
                    Column('id', Integer, Identity('liked_song_id_seq', start=1, increment=1), primary_key=True),
                    Column('song_id', None, ForeignKey('songs.genius_id')),
                    Column('user_id', None, ForeignKey('users.id'))
                    )