""" test_resource_manager

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2020-01-06
:Copyright: 2020, Karr Lab
:License: MIT
"""

import pytest
import biosimulations_dispatch.config as config
from biosimulations_dispatch.resource_manager import ResourceManager
from bson.objectid import ObjectId

from biosimulations_dispatch.utils import IdExistsError, DoesNotExistError


@pytest.fixture(scope="module")
def concreteManager():
    class concreteManager(ResourceManager):
        def _create(self, **kwargs):
            resource = super()._create(**kwargs)
            test_kwarg = kwargs.get("test_kwarg")
            concrete = {"test_kwarg": test_kwarg}
            resource.update(concrete)
            return resource
    cm = concreteManager(
        username=config.TestConfig.USERNAME,
        password=config.TestConfig.PASSWORD,
        host=config.TestConfig.SERVER,
        database=config.TestConfig.DATABASE,
        authSource="admin",
        collection="test_collection")
    return cm


class TestResourceManagerConstruction:
    def test_construction(self, concreteManager):
        assert(isinstance(concreteManager, ResourceManager))


class TestResourceCreation:
    def test_update_time(self):
        pass

    def test_create_time(self):
        pass


class TestResourceManagerAddMethods:

    @pytest.fixture(autouse=True)
    def clean_db(self, concreteManager):
        concreteManager.collection.delete_many({})

    def test_add_one(self, concreteManager):
        resource = {"id": "test_id", "name": "testName",
                    "private": False, "owner": "TestOwner"}
        concreteManager.add_one(**resource)
        new_resource = concreteManager.collection.find_one({"id": "test_id"})
        _id = new_resource.pop("_id")
        assert(_id)
        assert(new_resource["id"] == resource["id"])

    def test_add_one_generate_id(self, concreteManager):
        resource2 = {"name": "testName",
                     "private": False, "owner": "TestOwner"}
        new_resource = concreteManager.add_one(**resource2)
        _id = new_resource["id"]
        assert(_id)
        print(_id)
        new_resource = concreteManager.collection.find_one(
            {"_id": ObjectId(_id)})
        assert(new_resource)

    def test_add_one_raise_id_exists_error(self, concreteManager):
        resource = {"id": "duplicate_id", "name": "testName",
                    "private": False, "owner": "TestOwner"}
        new_resource = concreteManager.add_one(**resource)

        resource2 = {"id": "duplicate_id", "name": "testName",
                     "private": False, "owner": "TestOwner"}
        with pytest.raises(IdExistsError):
            assert(concreteManager.add_one(**resource2))


class TestResourceManagerGetMethods:
    @pytest.fixture(scope="class", autouse=True)
    def set_db(self, concreteManager):
        concreteManager.collection.delete_many({})
        model = {"id": "testModelId",
                 "owner": "testUsername", "private": False}
        model2 = {"id": "testModelId2",
                  "owner": "testUsername2", "private": False}

        model3 = {"id": "testModelId3",
                  "owner": "testUsername", "private": True}
        model4 = {"id": "testModelId4",
                  "owner": "testUsername2", "private": True}

        concreteManager.collection.insert_one(model)
        concreteManager.collection.insert_one(model2)
        concreteManager.collection.insert_one(model3)
        concreteManager.collection.insert_one(model4)

    def test_get_all(self, concreteManager):

        resources = concreteManager.get_all()
        assert(len(resources) == 4)
        assert(resources[0]["id"] == "testModelId")
        assert(resources[1]["id"] == "testModelId2")
        assert(resources[2]["id"] == "testModelId3")
        assert(resources[3]["id"] == "testModelId4")
        # Confirm that the _id field is removed
        with pytest.raises(KeyError):
            assert resources[0]["_id"]

    def test_get_by_identifier(self, concreteManager):
        get = concreteManager.get_by_identifier(
            identifier="testModelId3")
        assert(get["id"] == "testModelId3")

    def test_get_identifier_non_existant(self, concreteManager):
        with pytest.raises(DoesNotExistError):
            assert(concreteManager.get_by_identifier(identifier="NonExistent"))

    def test_get_all_public(self, concreteManager):
        resources = concreteManager.get_all_public()
        assert(len(resources) == 2)
        assert(resources[0]["id"] == "testModelId")
        assert(resources[1]["id"] == "testModelId2")
        # Confirm that the _id field is removed
        with pytest.raises(KeyError):
            assert resources[0]["_id"]

    def test_get_private_by_owner(self, concreteManager):
        resources = concreteManager.get_private_by_owner("testUsername2")
        assert(len(resources) == 1)
        assert(resources[0]["id"] == "testModelId4")\
            # Confirm that the _id field is removed
        with pytest.raises(KeyError):
            assert resources[0]["_id"]

    def test_get_by_owner(self, concreteManager):
        resources = concreteManager.get_by_owner("testUsername2")
        assert(len(resources) == 2)
        assert(resources[0]["id"] == "testModelId2")
        assert(resources[1]["id"] == "testModelId4")
        # Confirm that the _id field is removed
        with pytest.raises(KeyError):
            assert resources[0]["_id"]

    def test_get_public_by_owner(self, concreteManager):
        resources = concreteManager.get_public_by_owner("testUsername2")
        assert(len(resources) == 1)
        assert(resources[0]["id"] == "testModelId2")
        # Confirm that the _id field is removed
        with pytest.raises(KeyError):
            assert resources[0]["_id"]


class TestResourceManagerUpdateMethods:
    @pytest.fixture(scope="class", autouse=True)
    def set_db(self, concreteManager):
        concreteManager.collection.delete_many({})
        model = {"id": "testModelId",
                 "owner": "testUsername", "private": False}
        model2 = {"id": "testModelId2",
                  "owner": "testUsername2", "private": False}

        model3 = {"id": "testModelId3",
                  "owner": "testUsername", "private": True}
        model4 = {"id": "testModelId4",
                  "owner": "testUsername2", "private": True}

        concreteManager.collection.insert_one(model)
        concreteManager.collection.insert_one(model2)
        concreteManager.collection.insert_one(model3)
        concreteManager.collection.insert_one(model4)

    def test_update_one_non_existant(self, concreteManager):
        with pytest.raises(DoesNotExistError):
            concreteManager.update_one(identifier="nonExistantID", **{})

    def test_update_one(self, concreteManager):
        model3 = {"id": "testModelId3", "name": "NewName",
                  "owner": "testUsername", "private": True}
        concreteManager.update_one(identifier="testModelId3", **model3)

        updated_model = concreteManager.collection.find_one(model3)
        updated_model.pop("_id")
        assert(updated_model["name"] == model3["name"])

    def test_update_one_dup_id(self, concreteManager):
        model3 = {"id": "testModelId2", "name": "NewName",
                  "owner": "testUsername", "private": True}
        with pytest.raises(IdExistsError):
            assert(concreteManager.update_one(
                identifier="testModelId3", **model3))
