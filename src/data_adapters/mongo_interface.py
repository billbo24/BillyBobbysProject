from pymongo.mongo_client import MongoClient
from src.config import get_mongo_host

client = MongoClient(get_mongo_host())

def test_insert_data(client: MongoClient):


    #Beb needs to learn how to comment
    db = client['beb_database'] #Creates database, or accesses it if it exists
    # col = db.create_collection('first_test')
    col = db['first_test']

    col.insert_one({'100': '10000'})
    col.insert_one({'Testing': ['1', '2', '3']})
    col.insert_one({'6': '10'})


def get_supply_info(client: MongoClient):

    db = client.get_database('sample_supplies')
    col = db['sales']

    data = col.find({})
    finalData = list(data)

    print(finalData[0])


def push_to_mongo(client: MongoClient,data_to_push,database,collection):
    #This will take JSON data and push it to mongo
    #I suppose if something isn't JSON then we should break it
    #As best I can tell JSON is really just...a dictionary???
    if isinstance(data_to_push,dict) == False:
        #Not a dictionary...no dice
        print("Not JSON data, beat it loser")
        return False
    
    #Alright, after some playing around it seems like the fundamental
    #unit of data here are dictionaries, but referred to as documents.  
    #A standard python array containing all the dictionaries we want
    #to push will allow us to use the col.insert_many() function
    
    
    return False

