from pymongo.mongo_client import MongoClient
from src.config import get_mongo_host

client = MongoClient(get_mongo_host())
print(client.list_database_names())

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
