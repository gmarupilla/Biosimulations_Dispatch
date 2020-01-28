""" test_model_manager

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-12-26
:Copyright: 2019, Karr Lab
:License: MIT
"""
import pytest
import biosimulations_dispatch.core as core
import biosimulations_dispatch.utils as util


from biosimulations_dispatch.resource_manager import ResourceManager


@pytest.fixture(scope="module")
def modelManager():
    return core.DBManager(database="python_test_db").model_manager()


class TestModelManagerConstruction:
    def test_construction(self, modelManager):
        assert(isinstance(modelManager, ResourceManager))


class TestModelCreation:
    def test_create(self, modelManager):
        model = modelManager._create()
        assert(isinstance(model, dict))
