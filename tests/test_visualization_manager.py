""" test_visualization_manager

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
def visualizationManager():
    return core.DBManager(database="python_test_db").visualization_manager()


class TestVisualizationManagerConstruction:
    def test_construction(self, visualizationManager):
        assert(isinstance(visualizationManager, ResourceManager))


class TestVisualizationCreation:
    def test_create(self, visualizationManager):
        vis = visualizationManager._create()
        assert(isinstance(vis, dict))
