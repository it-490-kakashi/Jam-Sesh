from .creds import db #DO NOT CHANGE!!
from sqlalchemy import Table, Column, String, MetaData, Integer, Identity, ForeignKey, Sequence


# SQL Expression Language
meta = MetaData(db)
basic_user = Table('users', meta,
                   Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
                   Column('first_name', String),
                   Column('last_name', String),
                   Column('email', String),
                   Column('username', String),
                   Column('password', String)
                   )

song_list = Table('songs', meta,
                  Column('id', Integer, Sequence('song_id_seq'), primary_key=True),
                  Column('name', String),
                  Column('artist', String),
                  Column('genre', String)
                  )

liked_songs = Table('liked_songs', meta,
                    Column('id', Integer, Sequence('liked_song_id_seq'), primary_key=True),
                    Column('song_id', None, ForeignKey('songs.id')),
                    Column('user_id', None, ForeignKey('users.id'))
                    )
