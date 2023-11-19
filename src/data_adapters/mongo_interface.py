from pymongo.mongo_client import MongoClient
from src.config import get_mongo_host

def get_default_mongo_client() -> MongoClient:
    return MongoClient(get_mongo_host())

def test_insert_data(client: MongoClient):

    db = client['beb_database']
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
