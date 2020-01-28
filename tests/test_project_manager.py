""" test_project_manager

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
def projectManager():
    return core.DBManager(database="python_test_db").project_manager()


class TestProjectManagerConstruction:
    def test_construction(self, projectManager):
        assert(isinstance(projectManager, ResourceManager))


class TestProjectCreation:
    def test_create(self, projectManager):
        project = projectManager._create()
        assert(isinstance(project, dict))
