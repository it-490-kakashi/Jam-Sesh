from creds import db
from models import basic_user
import logging

logging.basicConfig(filename='log_file.log', encoding='utf-8', format='%(levelname)s:%(message)s', level=logging.DEBUG)


def by_id(user_id):
    with db.connect() as conn:
        user = basic_user.select().where(basic_user.c.id == user_id)
        result = conn.execute(user)
        logging.debug('ID: ' + user_id)
        if len(result.fetchall()) == 0:
            logging.error('No User Found')
            return False
        return True


def by_username(username):
    with db.connect() as conn:
        query = basic_user.select().where(basic_user.c.username == username)
        logging.debug('Username: ' + username)
        return conn.execute(query).fetchone() is not None  # Returns true if email found


def by_email(email):
    with db.connect() as conn:
        query = basic_user.select().where(basic_user.c.email == email)
        logging.debug('Email: ' + email)
        return conn.execute(query).fetchone() is not None  # Returns true if email found


def by_first_and_last(firstname, lastname):
    with db.connect() as conn:
        user = basic_user.select().where(basic_user.c.first_name == firstname & basic_user.c.last_name == lastname)
        result = conn.execute(user)
        logging.debug('First Name: ' + firstname)
        logging.debug('Last Name: ' + lastname)
        if len(result.fetchall()) == 0:
            logging.error('User Not Found')
            return False
    return True
