import pytest

import biosimulations_dispatch.core as core


def test_core_object():
    mongomanager = core.DBManager()
    assert(mongomanager)  # test object created


def test_returned_objects():
    usermanager = core.DBManager().user_manager()
    assert(usermanager)

    simulationmanager = core.DBManager().simulation_manager()
    assert(simulationmanager)

    modelsmanager = core.DBManager().model_manager()
    assert(modelsmanager)

    filesmanager = core.DBManager().file_manager()
    assert(filesmanager)
