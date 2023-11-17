import psycopg2 #to get this module use 'pip install psycopg2-binary', it requires Python 3
import pandas as pd

#Database Connection Parameters (*note - to actually connect I need to whitelist your IP address in AWS).
#TODO: normally it's bad form to save the hostname and password of your database in a public place like gitHub,
#there are people out there that scrape repos for this kind of stuff. We're just in a test phase for now and this 
#is pretty small scale so it should be fine, but ultimately we'll want to save these as environment variables on
#our own PCs.
_dbname = "billybobbys"
_user = "postgres"
_password = "password"
_host = "database-1.csjukvpunyct.us-east-1.rds.amazonaws.com"
_port = "5432"

#A method for adding a data from a Pandas DataFrame to an existing table of a PostgreSQL database.
#This method expects the columns of the DataFrame to have the same values as the existing tables,
#if they don't then an error will pop up and no data will be persisted
def add_data_frame_to_table(data: pd.DataFrame,table):
    #connect to the database
    print(data) #test
    print("\n")

    try:
        conn = psycopg2.connect(dbname = _dbname, user = _user, password = _password, host = _host, port = _port)
    except psycopg2.Error as e:
        print("Couldn't connect to the database, make sure credentials are correct and your IP has been whitelisted.")
        return

    #Open a cursor to perform db operations. Using the cursor we can type pute
    #SQL commands as shown below when creating a table
    cur = conn.cursor()

    #For now, drop the table every time we call this method and create it from scratch
    try:
        cur.execute("DROP TABLE IF EXISTS " + table + ";")
    except psycopg2.Error as e:
        print(e)

    #TODO Need to finish logic for the create table string, the insert string is done
    #We now create a new table with the given data. Postgresql needs the data type for each column
    #so this must be extracted from the data set
    create_string = "CREATE TABLE " + table + "(player_id SERIAL PRIMARY KEY, "
    insert_string = "INSERT INTO " + table + " ("

    #Start creating the execution string, starting with getting the column names
    for col in data:
        insert_string += (col + ", ")

    #After getting the column names insert each row from the data table one at a time
    insert_string = insert_string[:-2] + ") VALUES "

    for index,row in data.iterrows():
        insert_string += "("
        for data in row:
            #check to see if the data typs is a string, if so we need single quotes around it
            if isinstance(data, str): insert_string += "'" + data + "', "
            else: insert_string += str(data) + ", "

        insert_string = insert_string[:-2] + "), "

    insert_string = insert_string[:-2] + ";"

    #create a new test table
    # try:
    #     cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    # except psycopg2.Error as e:
    #     #if the database already exists we should get an alert about it
    #     print(e)


    # #commit all changes to persist them in the db
    # conn.commit()

    print(insert_string) #TEST

    #close the connection to the database
    conn.close()