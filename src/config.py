import os
from dotenv import load_dotenv

#Had the full filepath on my machine, but that's not helpful for everyone else.  
#Replace the .env string here
load_dotenv('.env')

def get_billy_bobbys_db_cred() -> dict[str]:
    # Gets credentials for Postgress DB

    dbname = os.environ['billybobbys_db']
    user = os.environ['billybobbys_user']
    password = os.environ['billybobbys_password']
    host = os.environ['billybobbys_host']
    port = os.environ['billybobbys_port']

    return dict(dbname=dbname, user=user, password=password, host=host, port=port)

def get_mongo_host() -> str:
    return os.environ['mongodb_host']