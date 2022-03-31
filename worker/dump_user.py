from models import basic_user
from creds import db
from datetime import datetime, date
import os
import json

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def create_dump():
    with db.connect() as conn:
        users = basic_user.select().where(basic_user.c.id > 0)
        users = conn.execute(users).fetchall()
        if users is not None:
            script_dir = os.path.dirname(__file__)
            rel_path = "/user_dump" + (datetime.now().strftime("%Y.%m.%d.%H.%M.%S")) + ".json"
            json_file = os.path.join(script_dir, rel_path)
            f = open(json_file, "x")
            users_list = []
            for item in users:
                users_list.append({'first_name':item.first_name, 'last_name':item.last_name, 'email':item.email, 'user_name':item.username})
            f.write(json.dumps(users_list))
            # print(users)
            print("jsonstring " + json.dumps(users_list))
            print("dump name is " + f.name)
            f.close()
            return "dump successful"
        return "dump unsuccessful"

def retrieve_latest_dump():
    script_dir = os.path.dirname(__file__)
    rel_path = "/"
    json_file = os.path.join(script_dir, rel_path)
    dir_list = os.listdir(json_file)
    print(json_file)
    latest_dump = ""
    for item in dir_list:
        temp_file = os.path.join(json_file, item)
        print(temp_file + " , " +  " , " + str(temp_file.__contains__("user_dump")) + " , " + str((latest_dump < temp_file)))
        if temp_file.__contains__("user_dump") and latest_dump < temp_file:
            latest_dump = temp_file
            print(latest_dump)
    if latest_dump != "":
        jsondata = json.load(open(latest_dump))
        return jsondata
    else:
        return None