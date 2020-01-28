""" test_user_manager

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
import pytest
import pymongo

import biosimulations_dispatch.core as core
import biosimulations_dispatch.utils as util

import biosimulations_dispatch.user_manager as user_manager


@pytest.fixture
def userManager():
    return core.DBManager(database="test").user_manager()


class TestUserManagerConstruction:

    def test_construction(self, userManager):
        assert(userManager)
        assert(isinstance(userManager, user_manager.UserManager))

    def test_mongoUtil_construction(self, userManager):
        assert(isinstance(userManager.mongo_manager, util.MongoUtil))

    def test_client_construction(self, userManager):
        assert(isinstance(userManager.client, pymongo.MongoClient))

    def test_db_construction(self, userManager):
        assert(isinstance(userManager.db, pymongo.database.Database))

    def test_collection_construction(self, userManager):
        assert(
            isinstance(
                userManager.collection,
                pymongo.collection.Collection))


class TestUserMethods:

    def test_add_one_user(self, userManager):
        user = {"userId": '002', "firstName": "bilal", "lastName": 'shaikh',
                "email": "bilal@bilal.com", "userName": "testuser"}
        userManager.add_one_user(
            userId=user["userId"],
            firstName=user["firstName"],
            lastName=user["lastName"],
            email=user["email"])
        get = userManager.collection.find_one({"_id": user["userId"]})
        assert(get)
        userManager.collection.delete_one({"_id": user["userId"]})

    def test_remove_one_user(self, userManager):
        user1 = {"name": "test"}
        user_id = userManager.collection.insert_one(user1).inserted_id
        userManager.remove_one_user(user1)
        get = userManager.collection.find_one({'_id': user_id})
        assert (get is None)

    def test_get_user_by_id(self, userManager):
        user1 = {'user_name': "the_test_name"}
        user_id = userManager.collection.insert_one(user1).inserted_id
        user = userManager.get_user_by_id(user_id)
        assert(user == user1)
        userManager.collection.delete_one({"_id": user_id})

    def test_get_user_by_name(self, userManager):
        user1 = {'userName': "the_test_name"}
        user_id = userManager.collection.insert_one(user1).inserted_id
        user = userManager.get_user_by_name("the_test_name")
        assert(user["_id"] == user_id)
        userManager.collection.delete_one({"_id": user_id})
