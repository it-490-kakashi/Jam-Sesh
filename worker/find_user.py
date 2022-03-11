from creds import db
from models import basic_user


def by_id(user_id):
    with db.connect() as conn:
        user = basic_user.select().where(basic_user.c.id == user_id)
        result = conn.execute(user)
        if len(result.fetchall()) == 0:
            return False
        return True


def by_username(username):
    with db.connect() as conn:
        user = basic_user.select().where(basic_user.c.username == username)
        result = conn.execute(user)
        if len(result.fetchall()) == 0:
            return False
        return True


def by_email(email):
    with db.connect() as conn:
        query = basic_user.select().where(basic_user.c.email == email)
        return conn.execute(query).fetchone() is not None  # Returns true if email found


def by_first_and_last(firstname, lastname):
    with db.connect() as conn:
        user = basic_user.select().where(basic_user.c.first_name == firstname & basic_user.c.last_name == lastname)
        result = conn.execute(user)
        if len(result.fetchall()) == 0:
            return False
    return True
