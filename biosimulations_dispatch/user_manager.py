""" user_manager to manage the users in the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch.utils import MongoUtil


class UserManager(object):

    def __init__(
            self,
            username=None,
            password=None,
            host="localhost",
            authSource="admin",
            database="test",
            collection="user"):
        self.mongo_manager = MongoUtil(
            host=host,
            username=username,
            password=password,
            authSource=authSource,
            db=database,
        )
        self.client, self.db, self.collection = self.mongo_manager.con_db(
            collection)

    def add_one_user(self, userId, firstName, lastName, email, userName=None):
        user = {"_id": userId, "firstName": firstName,
                "lastName": lastName, "userName": userName}
        user = self.collection.insert_one(user)
        # user = User(userId=userId, firstName=firstName,
        #            lastName=lastName, email=email, userName=userName)
        return user

    def remove_one_user(self, user):
        return self.collection.delete_one({'_id': user['_id']})

    def get_user_by_id(self, userId):
        return self.collection.find_one({'_id': userId})

    def get_user_by_name(self, name):
        return self.collection.find_one({"userName": name})

    def get_all_users(self):
        return self.collection.find()

    def replace_one_user(self, userId, user):
        self.collection.replace_one({"_id": userId}, user)
        return self.collection.find_one({'_id': userId})
