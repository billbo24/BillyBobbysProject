import os
from dotenv import load_dotenv

load_dotenv('.env')

def get_billy_bobbys_db_cred() -> dict[str]:
    # Gets credentials for Postgress DB

    dbname = os.environ['billybobbys_db']
    user = os.environ['billybobbys_user']
    password = os.environ['billybobbys_password']
    host = os.environ['billybobbys_host']
    port = os.environ['billybobbys_port']

    return dict(dbname=dbname, user=user, password=password, host=host, port=port)