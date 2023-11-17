import psycopg2

#database connection parameters (*note - to actually connect I need to whitelist your IP addres in AWS)
_dbname = "billybobbys"
_user = "postgres"
_password = "password"
_host = "database-1.csjukvpunyct.us-east-1.rds.amazonaws.com"
_port = "5432"

#connect to the database
try:
    conn = psycopg2.connect(dbname = _dbname, user = _user, password = _password, host = _host, port = _port)
except psycopg2.Error as e:
    print("Couldn't connect to the database")

#Open a cursor to perform db operations. Using the cursor we can type pute
#SQL commands as shown below when creating a table
cur = conn.cursor()

#create a new test table
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

#commit all changes to persist them in the db
conn.commit()

#close the connection to the database
conn.close()

print("Hello World!")