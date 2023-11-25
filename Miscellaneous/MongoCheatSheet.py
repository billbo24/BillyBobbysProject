#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Nov 18 19:53:34 2023

@author: williamfloyd
As I work with mongo it will be useful to keep a cheat sheet.  it's new
and I seem to get a lot of errors pretty often, so it's handy to keep notes.  I
seem to be pretty stuck think of data in terms of tables, when JSON doesn't 
*really* require that.  This will be a good place to play around 

A little mongo cheatsheet:
    We connect to a cluster, this is the client.  
        In SQL parlance, this seems most simlar to a server
    A cluster hosts numerous databases.  To see them use client.list_database_names()
        In SQL, this also seems similar to a databse (for example arl_ops at work)
    A database contains collections.  To see them use db.list_collection_names()
        These are like the tables in SQL
    Collections are composed of documents.  These appear to be more or less
    the most granular unit of data, and the biggest departure from SQL,
    which uses the humble row as its most granular unit of data
    

Also good to know:    
    It's a little different to "see" and interact with the data because 
    you're used to SQL.  Comments below explain how you might start poking
    and prodding a dataset pulled directly from mongodb
"""
import sys
# putting in the path for the src folder.  I think this lets us import the other stuff
sys.path.insert(0, '/Users/williamfloyd/Documents/PythonCode/BillyBobbysProject/')



#import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import src.data_adapters.mongo_interface as mi
import src.data_functions.functions as func
from src.config import get_mongo_host
import json
import pandas as pd
import random


#Had the full filepath on my machine, but that's not helpful for everyone else.  
#Replace the .env string here
load_dotenv('/Users/williamfloyd/Documents/PythonCode/BillyBobbysProject/env')

#Create a mongo client.  This connects to the one cluster we currently have
client = MongoClient(get_mongo_host())

#We can list all of the databases in a cluster like so:
print(client.list_database_names())


#beb has created a database, so I think I may try to add another collection
#going to make a cool dataset
names = ['Billy','Bobby','Beb','Jeb Bush']
weight = [180,155,160,300]
states_governed = [[],[],[],['Florida']]
Elections_lost = [[],[],[],[2012,2016]]
Languages_Spoken = [['English'],['English'],['English'],['English','Spanish']]
Loser = [30,30,30,9001]


billy_collection = []
for i in range(len(names)):
    start = {}
    start['Name'] = names[i]
    start['Weight'] = weight[i]
    start['states_governed'] = states_governed[i]
    start['Elections_lost'] = Elections_lost[i]
    start['Languages_Spoken'] = Languages_Spoken[i]
    start['Loser Score'] = Loser[i]
    billy_collection.append(start)

my_collection = json.dumps(billy_collection)
   
#This lists the databases
dbs = client.list_database_names()


#Now I'd like to create my own table, this sets our database
db = client['beb_database']

#This is how you list the collections within a database
cols = db.list_collection_names()


#Apparently it's like a dictionary.  You just kinda...do it lol
col = db['Billy_Data']



#Now we can insert many objects at once using the insert_many function
#Note that I believe it has to be a vector of dictionaries.  
#col.insert_many(billy_collection)

#This is an example of what a query looks like
query = {}

#You can leave the parentheses blank or put {} as a "find all" 
cursor = col.find(query)  # You can add a query parameter if needed
data = list(cursor)
df = pd.DataFrame(data)
df_expand = df.explode('Languages_Spoken')



#Lets experiment pushing a pandas array
#I think this would resemble what a "push pandas" function would look like
num_rows = 100
nums = [int(i) for i in range(num_rows)]
my_data = pd.DataFrame(nums,columns=['student number'])
my_data['vertical leap'] = [random.normalvariate(25, 7) for i in range(num_rows)]
my_data['SAT scores'] = [10*(int(random.uniform(700, 1600))//10) for i in range(num_rows)] #eat shit writing section
my_data['Excels in sports'] = [True if random.uniform(0, 1) < 0.1 else False for i in range(num_rows)]


#Pandas makes this way easier
#orient splits by record.  If we leave it blank it does it by column
a = my_data.to_json(orient='records')
#This doesn't work though because it's actually a long string
#This puts it in perfect format to load into mongo
b = json.loads(a) 

c = func.prepare_pandas_for_mongo(my_data)

#col.insert_many(b)


#Now I think I can delete documents like so:
#Yes this worked! The inside bit is the filtering    
#col.delete_one({ 'student number': { "$eq": 0 }})




def flatten_array(df):
    # Identify columns with arrays
    array_columns = df.applymap(lambda x: isinstance(x, list)).any()
    
    # Create a list of columns with arrays
    array_columns_list = array_columns[array_columns].index.tolist()
    
    print(array_columns_list)




col = db['Billy_Data']



#Now we can insert many objects at once using dfthe insert_many function
#Note that I believe it has to be a vector of dictionaries.  
#col.insert_many(billy_collection)

#This is an example of what a query looks like
query = {}

#You can leave the parentheses blank or put {} as a "find all" 
cursor = col.find(query)  # You can add a query parameter if needed
data = list(cursor)
df = pd.DataFrame(data)

flatten_array(df)
