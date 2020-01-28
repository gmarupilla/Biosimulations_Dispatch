""" test_chart_manager

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
def chartManager():
    return core.DBManager(database="python_test_db").chart_manager()


class TestchartManagerConstruction:
    def test_construction(self, chartManager):
        assert(isinstance(chartManager, ResourceManager))


class TestChartCreation:
    def test_create(self, chartManager):
        chart = chartManager._create()
        assert(isinstance(chart, dict))
