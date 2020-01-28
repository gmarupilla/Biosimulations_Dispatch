""" Tests for the file manager

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-13
:Copyright: 2019, Karr Lab
:License: MIT
"""

import biosimulations_dispatch.core as core
import biosimulations_dispatch.utils as util

import biosimulations_dispatch.file_manager as file_manager

import pymongo
import gridfs
import pytest


@pytest.fixture
def fileManager():
    return core.DBManager().file_manager()


class TestFileManagerConstruction:

    def test_construction(self, fileManager):
        assert(fileManager)
        assert(isinstance(fileManager, file_manager.FileManager))

    def test_mongoUtil_construction(self, fileManager):
        assert(isinstance(fileManager.mongo_manager, util.MongoUtil))

    def test_client_constrcution(self, fileManager):
        assert(isinstance(fileManager.client, pymongo.MongoClient))

    def test_db_coonstruction(self, fileManager):
        assert(isinstance(fileManager.db, pymongo.database.Database))

    def test_collection_construction(self, fileManager):
        assert(
            isinstance(
                fileManager.collection,
                pymongo.collection.Collection))


class TestFileMethods:
    @pytest.fixture
    def BinaryFile(self):
        return open("tests/test_file.txt", 'rb')

    @pytest.fixture
    def File(self):
        return open("tests/test_file.txt", 'rb')

    @pytest.fixture
    def fs(self, fileManager):
        return gridfs.GridFS(fileManager.db)

    def test_add_file_to_db(self, fileManager, BinaryFile, File, fs):
        print(type(File))
        file_id = fileManager.add_file_to_db(BinaryFile, "test.file")
        pulled_file = fs.get(file_id)
        assert(pulled_file.read() == File.read())
