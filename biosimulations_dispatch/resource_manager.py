""" Resource Manager provides a base class for all the resources in the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2020-01-06
:Copyright: 2020, Karr Lab
:License: MIT
"""

from abc import ABC, abstractmethod
from bson.objectid import ObjectId
import pymongo
from biosimulations_dispatch.utils import IdExistsError, DoesNotExistError, MongoUtil
import datetime
from .utils import genAccessToken
from .utils import parseTime


class ResourceManager(ABC):
    def __init__(
            self,
            username,
            password,
            host,
            authSource,
            database,
            collection):
        self.mongo_manager = MongoUtil(
            host=host,
            username=username,
            password=password,
            authSource=authSource,
            db=database,
        )
        self.client, self.db, self.collection = self.mongo_manager.con_db(
            collection)

    @abstractmethod
    def _create(self, **kwargs):
        resourceId = kwargs.get("id", None)
        parent = kwargs.get('parent', None)
        name = kwargs.get("name", None)
        image = kwargs.get("image", None)
        owner = kwargs.get("owner", "google-oauth2|101683931106741052527")
        description = kwargs.get("description")
        summary = kwargs.get("summary")
        private = kwargs.get("private", False)
        published = kwargs.get("published", False)
        tags = kwargs.get("tags", [])
        created = kwargs.get("created")
        if (created):
            created = parseTime(created)
        else:
            created = datetime.datetime.utcnow()
        updated = datetime.datetime.utcnow()
        identifiers = kwargs.get("identifiers", [])
        accessToken = kwargs.get("accessToken", genAccessToken())
        license = kwargs.get("license", "mit")
        references = kwargs.get('references', [])
        authors = kwargs.get(
            "authors", [{"firstName": owner, "lastName": "", "middleName": ""}])
        resource = {
            "id": resourceId,
            "name": name,
            "image": image,
            "owner": owner,
            "description": description,
            "private": private,
            "published": published,
            "summary": summary,
            "tags": tags,
            "created": created,
            "updated": updated,
            "identifiers": identifiers,
            "accessToken": accessToken,
            "license": license,
            "authors": authors,
            "parent": parent,
            "references": references}
        return resource

    def add_one(self, **kwargs):
        resource = self._create(**kwargs)
        _id = ObjectId()

        if resource["id"] is None:
            resource["id"] = str(_id)
            resource["_id"] = _id

        try:
            resource = self.collection.insert_one(resource)
        except pymongo.errors.DuplicateKeyError:
            raise IdExistsError()

        resource = self.collection.find_one(
            {"_id": resource.inserted_id}, {'_id': False})

        return resource

    def get_all(self):
        return list(self.collection.find({}, {'_id': False}))

    def get_all_public(self):
        return list(self.collection.find({"private": False}, {'_id': False}))

    def get_private_by_owner(self, owner):
        return list(self.collection.find(
            {"private": True, "owner": owner}, {'_id': False}))

    def get_by_owner(self, owner):
        return list(self.collection.find({"owner": owner}, {'_id': False}))

    def get_public_by_owner(self, owner):
        return list(self.collection.find(
            {"private": False, "owner": owner}, {'_id': False}))

    def get_by_identifier(self, identifier):
        resource = self.collection.find_one({"id": identifier}, {'_id': False})
        if (resource is None):
            raise DoesNotExistError()
        return resource

    def update_one(self, identifier, **kwargs):
        resource = self.collection.find_one({"id": identifier})

        if resource is None:
            raise DoesNotExistError("Resource does not exist")

        # Don't override created
        kwargs["created"] = resource.get(
            "created")

        _id = resource["_id"]
        updatedResource = self._create(**kwargs)

        try:
            self.collection.replace_one({"_id": _id}, updatedResource)
        except pymongo.errors.DuplicateKeyError:
            raise IdExistsError()

        resource = self.collection.find_one({"_id": _id}, {'_id': False})

        if resource is None:
            raise Exception("Could not update")
        return resource
