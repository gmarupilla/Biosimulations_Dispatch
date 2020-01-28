""" Utilities for the dispatch package

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
import pymongo
from bson import decode_all
import hashlib
from genson import SchemaBuilder
import random
import string
import dateutil.parser
import datetime


def genAccessToken():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(16))


def parseTime(time):
    if isinstance(time, datetime.datetime):
        return time
    return dateutil.parser.parse(time)


class IdExistsError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, "The chosen ID already exists", **kwargs)


class DoesNotExistError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, "The resource does not exist", **kwargs)


class MongoUtil:
    """Utilities to connect to a mongo database
    :Author: Zhouyang Lian <zhouyang.lian@familian.life>
    :Date: 2019-11-07
    :Copyright: 2019, Karr Lab
    :License: MIT
    """

    def __init__(
            self,
            cache_dirname=None,
            host=None,
            replicaSet=None,
            db='test',
            verbose=False,
            max_entries=float('inf'),
            username=None,
            password=None,
            authSource='admin',
            readPreference='primary'):

        self.client = pymongo.MongoClient(
            host=host, replicaSet=replicaSet,
            username=username, password=password,
            authSource=authSource, readPreference=readPreference)
        self.db_obj = self.client.get_database(db)

    def list_all_collections(self):
        '''List all non-system collections within database
        '''

        return self.db_obj.list_collection_names()

    def con_db(self, collection_str):
        try:
            collection = self.db_obj[collection_str]
            return (self.client, self.db_obj, collection)
        except pymongo.errors.ConnectionFailure:
            return ('Server not available')
        except pymongo.errors.ServerSelectionTimeoutError:
            return ('Server timeout')

    def get_schema(self, collection_str):
        '''Get schema of a collection
           removed '_id' from collection due to its object type
           and universality
        '''
        _, _, collection = self.con_db(collection_str)
        doc = collection.find_one({})
        builder = SchemaBuilder()
        del doc['_id']
        builder.add_object(doc)
        return builder.to_schema()

    def flatten_collection(self, collection_str):
        '''Flatten a collection
            c is ommitted because it does not have a non-object
            value associated with it
        '''
        _, _, collection = self.con_db(collection_str)

        pipeline = [
            {"$addFields": {"subdoc.a": "$a"}},
            {"$replaceRoot": {"newRoot": "$subdoc"}}
        ]
        flat_col = collection.aggregate(pipeline)
        return flat_col
