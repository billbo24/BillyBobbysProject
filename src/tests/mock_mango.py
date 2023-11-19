from collections import defaultdict
from datetime import datetime
import os
from typing import Iterable
import unittest
import pydantic

from src.data_adapters.mongo_interface import get_default_mongo_client
from src.data_adapters.csv_interface import read_csv_dict

class Event(pydantic.BaseModel):
    country: str
    description: str
    event_date: datetime

class Package(pydantic.BaseModel):
    package_id: str
    length: float
    width: float
    height: float
    weight: float
    events: list[Event] = None


def create_test_package_data(fp: str) -> list[dict[str: str]]:
    package_header_conversions = {'PackageID': 'package_id', 'Length': 'length', 'Width': 'width', 'Height': 'height', 'Weight': 'weight'}
    return read_csv_dict(fp, package_header_conversions)

def create_test_event_data(fp: str) -> list[dict[str: str]]:
    event_header_conversions = {'PackageID': 'package_id', 'Country': 'country', 'Description': 'description', 'EventDateUtc': 'event_date'}
    return read_csv_dict(fp, event_header_conversions)

def create_packages(package_data: list[dict[str: str]], event_data: list[dict[str: str]]) -> Iterable[Package]:
    events = defaultdict(list)
    for event in event_data:
        events[event['package_id']].append(Event(country=event['country'], description=event['description'], event_date=event['event_date']))

    for package in package_data:
        package_events = events.get(package['package_id'], [])
        yield Package(**package, events=package_events)

def convertPackagesToDict(packages: list[Package]) -> dict:
    for package in packages:
        print(package.model_dump())


class InsertShippingDataTest(unittest.TestCase):

    def test_create_db(self):
        client = get_default_mongo_client()
        db = client['shipping_data']
        col = db.create_collection('packages')

    def test_list_db(self):
        client = get_default_mongo_client()
        print(client.list_database_names())

    def test_convert_packages_to_dict(self):
        package_fp = os.path.join('testdata', 'Fake Package Data.csv')
        event_fp = os.path.join('testdata', 'Fake Event Data.csv')

        packages = list(create_packages(create_test_package_data(package_fp), create_test_event_data(event_fp)))
        convertPackagesToDict(packages)
        
    def test_insert_data(self):
        package_fp = os.path.join('testdata', 'Fake Package Data.csv')
        event_fp = os.path.join('testdata', 'Fake Event Data.csv')

        packages = [package.model_dump() for package in create_packages(create_test_package_data(package_fp), create_test_event_data(event_fp))]

        client = get_default_mongo_client()
        db = client['shipping_data']
        col = db['packages']
        col.insert_many(packages)


class ShippingQueryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = get_default_mongo_client()
        cls.db = cls.client['shipping_data']
        cls.col = cls.db['packages']

    def test_query_specific_package(self):
        print('')
        print('*** PACKAGE DATA FOR PACKAGE ID 14769A0001611061 ***')
        print('')

        data = self.col.find( {'package_id': '14769A0001611061'} )
        print(next(data))
    
    def test_query_packages_with_us_events(self):
        print('')
        print('*** PACKAGE DATA FOR PACKAGES WITH US BASED EVENTS ***')
        print('')

        data = list(self.col.find( {'events.country': 'US'} ))
        print(len(data))
        print(data[0])
        print(data[1])

    def test_query_packages_based_on_height(self):
        print('')
        print('*** PACKAGE DATA FOR PACKAGES WITH HEIGHTS GREATER THAN 12 INCHES***')
        print('')

        data = list(self.col.find( {'height': {'$gt': 12} }))
        print(len(data))
        print(data[0])
        print(data[1])    

    def test_query_packages_based_on_height_or_weight(self):
        print('')
        print('*** PACKAGE DATA FOR PACKAGES WITH HEIGHTS GREATER THAN 12 INCHES OR GREATER THAN 5 LBS***')
        print('')

        data = list(self.col.find( {'$or': [{'height': {'$gt': 12} }, {'weight': {'$gt': 5}}] }))
        print(len(data))
        print(data[0])
        print(data[1])   