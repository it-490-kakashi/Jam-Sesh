from sqlalchemy import exc
from creds import db
from models import basic_user, logged_in_user
from find_user import by_username, by_email
from basic_crud import get_user
import secrets
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt
from datetime import datetime, timedelta


def login(username, password):
    with db.connect() as conn:
        query = basic_user.select().where(basic_user.c.username == username)
        user = conn.execute(query).fetchone()
        if user is not None and check_hash_password(password, user.password):
            # Hash Password
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

                return [user_found, session_token]
            return [user_found]  # Sending as array since front_end wont know if it's array or not


def logout(session_token):
    with db.connect() as conn:
        # Write code
        if user_session_valid(session_token):
            query = logged_in_user.delete().where(logged_in_user.c.session_token == session_token)
            conn.execute(query)
            return True
        return False


def register(username, firstname, lastname, email, password):
    with db.connect() as conn:
        if not by_email(email):
            result_data = basic_user.insert().values(first_name=firstname,
                                                     last_name=lastname,
                                                     username=username,
                                                     email=email,
                                                     password=password,
                                                     )
            conn.execute(result_data)
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
        return conn.execute(query).fetchone() is not None


def user_info_from_session_token(session_token):
    with db.connect() as conn:
        query = logged_in_user.select().where(logged_in_user.c.session_token == session_token)
        result = conn.execute(query).fetchone()
        if result is not None:
            user_id = result[0]
            return get_user(user_id)
        return None

def check_hash_password(password, hash_pass):
    return check_password_hash(hash_pass, password)

def hash_password(password):
    return generate_password_hash(password)