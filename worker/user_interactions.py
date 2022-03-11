from sqlalchemy import exc
from creds import db
from models import basic_user, logged_in_user
from find_user import by_username, by_email
import secrets
from datetime import datetime, timedelta


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
                user_id = conn.execute(user_id).fetchone()
                print("Hello there!")
                add_login = logged_in_user.insert().values(user_id=user_id[0],
                                                           session_token=secrets.token_hex(5),
                                                           token_expiry=datetime.now() + timedelta(days=30))
                conn.execute(add_login)
            return user_found


def logout(username):
    with db.connect() as conn:
        # Write code
        return ""


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
