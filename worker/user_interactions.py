from sqlalchemy import exc
from creds import db
from models import basic_user, logged_in_user
from find_user import by_username, by_email
from basic_crud import get_user
import secrets
from datetime import datetime, timedelta
import hashlib
import logging, sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                              '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def login(username, password):
    with db.connect() as conn:
        if by_username(username):
            query = basic_user.select().where(basic_user.c.username == username, basic_user.c.password == password)
            result = conn.execute(query).fetchone()
            user_found = result is not None  # Return true if result has content
            if user_found:
                update_time = basic_user.update().where(basic_user.c.username == username, basic_user.c.password ==
                                                        password).values(last_login=datetime.now())
                conn.execute(update_time)
                user_id = basic_user.select().where(basic_user.c.username == username,
                                                    basic_user.c.password == password)
                user_id = conn.execute(user_id).fetchone()[0]

                session_token = user_session_token(user_id)
                logger.info('Session Cookie Generated')
                return [user_found, session_token]
            logger.info('User Login')
            return [user_found]  # Sending as array since front_end wont know if it's array or not


def logout(session_token):
    with db.connect() as conn:
        # Write code
        if user_session_valid(session_token):
            query = logged_in_user.delete().where(logged_in_user.c.session_token == session_token)
            conn.execute(query)
            logger.info('User Logged Out')
            return True
        return False


def register(username, firstname, lastname, email, password):
    with db.connect() as conn:
        if not by_email(email):
            h = hashlib.sha256(password.encode())
            hashword = h.hexdigest()
            result_data = basic_user.insert().values(first_name=firstname,
                                                     last_name=lastname,
                                                     username=username,
                                                     email=email,
                                                     password=password,
                                                     hashed=hashword
                                                     )
            conn.execute(result_data)
            logger.info('User Successfully Registered')
            return True
        return False


def user_session_token(user_id):
    with db.connect() as conn:
        query = logged_in_user.select().where(logged_in_user.c.user_id == user_id)
        if conn.execute(query).fetchone() is None:
            session_token = secrets.token_hex(5)

            add_login = logged_in_user.insert().values(user_id=user_id,
                                                       session_token=session_token,
                                                       token_expiry=datetime.now() + timedelta(days=30))
            conn.execute(add_login)

            return session_token
        return conn.execute(query).fetchone()[1]


def user_session_valid(session_token):
    with db.connect() as conn:
        query = logged_in_user.select().where(logged_in_user.c.session_token == session_token)
        logger.info('User Session Valid')
        return conn.execute(query).fetchone() is not None


def user_info_from_session_token(session_token):
    with db.connect() as conn:
        query = logged_in_user.select().where(logged_in_user.c.session_token == session_token)
        result = conn.execute(query).fetchone()
        if result is not None:
            user_id = result[0]

            return get_user(user_id)

        return None
