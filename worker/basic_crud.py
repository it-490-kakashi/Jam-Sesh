from sqlalchemy import exc
from creds import db
from models import basic_user
import find_user as find_user



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

            return "User Added"
        except exc.SQLAlchemyError:

            return "ERROR: " + str(exc.SQLAlchemyError)


# Read
def get_users():
    with db.connect() as conn:
        try:
            select = basic_user.select()
            result = conn.execute(select)

            return result.fetchall()
        except exc.SQLAlchemyError as e:

            return "ERROR: " + str(e)


# Read user @ id
def get_user(user_id):
    with db.connect() as conn:
        try:
            select = basic_user.select().where(basic_user.c.id == user_id)

            return conn.execute(select).fetchone()
        except exc.SQLAlchemyError as e:

            return "ERROR: " + str(e)


# Update first/last @ id
def update_user(user_id, first, last):
    with db.connect() as conn:
        try:
            if find_user.by_id(user_id):
                update = basic_user.update().where(basic_user.c.id == user_id).values(first=first, last=last)
                conn.execute(update)

                return f"User @ id:{user_id} was updated"

            return f"ERROR: User @ id:{user_id} not found"
        except exc.SQLAlchemyError:

            return "ERROR: " + str(exc.SQLAlchemyError)


def delete_user(user_id):
    with db.connect() as conn:
        if find_user.by_id(user_id):
            conn.execute(basic_user.delete().where(basic_user.c.id == user_id))

            return f"Deleted user @ id:{user_id}"

        return f"ERROR: User @ id:{user_id} is not found"
