from sqlalchemy import exc
from creds import db
from models import basic_user
import find_user as find_user
import logging

logging.basicConfig(filename='log_file.log', encoding='utf-8', format='%(levelname)s:%(message)s', level=logging.DEBUG)


# Create
def add_user(first_name, last_name, email, username, password):
    with db.connect() as conn:
        try:
            new_user = basic_user.insert().values(first_name=first_name,
                                                  last_name=last_name,
                                                  email=email,
                                                  username=username,
                                                  password=password)
            conn.execute(new_user)
            logging.debug('User Added')
            return "User Added"
        except exc.SQLAlchemyError:
            logging.error(str(exc.SQLAlchemyError))
            return "ERROR: " + str(exc.SQLAlchemyError)


# Read
def get_users():
    with db.connect() as conn:
        try:
            select = basic_user.select()
            result = conn.execute(select)
            logging.debug('Users Retrieved')
            return result.fetchall()
        except exc.SQLAlchemyError as e:
            logging.error(str(e))
            return "ERROR: " + str(e)


# Read user @ id
def get_user(user_id):
    with db.connect() as conn:
        try:
            select = basic_user.select().where(basic_user.c.id == user_id)
            logging.debug('User ' + select + ' Found')
            return conn.execute(select).fetchone()
        except exc.SQLAlchemyError as e:
            logging.error(str(e))
            return "ERROR: " + str(e)


# Update first/last @ id
def update_user(user_id, first, last):
    with db.connect() as conn:
        try:
            if find_user.by_id(user_id):
                update = basic_user.update().where(basic_user.c.id == user_id).values(first=first, last=last)
                conn.execute(update)
                logging.debug('User ' + user_id + ' was updated')
                return f"User @ id:{user_id} was updated"
            logging.error('User ' + user_id + ' not found')
            return f"ERROR: User @ id:{user_id} not found"
        except exc.SQLAlchemyError:
            logging.error(str(exc.SQLAlchemyError))
            return "ERROR: " + str(exc.SQLAlchemyError)


def delete_user(user_id):
    with db.connect() as conn:
        if find_user.by_id(user_id):
            conn.execute(basic_user.delete().where(basic_user.c.id == user_id))
            logging.debug('Deleted user: ' + user_id)
            return f"Deleted user @ id:{user_id}"
        logging.error('User ' + user_id + ' not found')
        return f"ERROR: User @ id:{user_id} is not found"
