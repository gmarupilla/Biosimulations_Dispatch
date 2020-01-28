""" Visualization manager to manage Visualizations in the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch.resource_manager import ResourceManager


class VisualizationManager(ResourceManager):

    def _create(self, **kwargs):

        resource = super()._create(**kwargs)
        data = kwargs.get("data", [])
        columns = kwargs.get("columns", 1)
        layout = kwargs.get("layout", [])
        Visualization = {"data": data, "layout": layout, "columns": columns}
        resource.update((Visualization))

        return resource
