from sqlalchemy import exc
from creds import db
from models import basic_user
from find_user import by_username


def login(username, password):
    with db.connect() as conn:
        if by_username(username):
            user = basic_user.select().where(basic_user.c.username == username & basic_user.c.password == password)
            if len(user.fetchall()) == 1:
                info = {
                    'session_id': 1231241,  # TODO: Generate token
                    'user_info': {
                        "username": username,
                        "full_name": f"{user['first']} {user['last']}"
                    }
                }
                # Generate session id
                # Compile user info & session id into directory
                return info
