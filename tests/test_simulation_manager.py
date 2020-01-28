""" test_simulation_manager

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
def simulationManager():
    return core.DBManager(database="python_test_db").simulation_manager()


class TestSimulationManagerConstruction:
    def test_construction(self, simulationManager):
        assert(isinstance(simulationManager, ResourceManager))


class TestSimulationCreation:
    def test_create(self, simulationManager):
        simulation = simulationManager._create()
        assert(isinstance(simulation, dict))
