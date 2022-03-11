from sqlalchemy import exc
from creds import db
from models import basic_user
from find_user import by_username, by_email
import secrets


def login(username, password):
    with db.connect() as conn:
        if by_username(username):
            user = basic_user.select().where(basic_user.c.username == username & basic_user.c.password == password)
            if len(user.fetchall()) == 1:
                info = {
                    "session_id": secrets.token_hex(5),  # Generated session id
                    "user_info": {
                        "username": username,
                        "password": password

                    }
                }

                users_data = basic_user.select().where(basic_user.c.username == username and basic_user.c.password == password)
                result = conn.execute(users_data)
                if len(result.fetchall() == 0):
                    return False
                return True

            else:
                return "Error!"


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
