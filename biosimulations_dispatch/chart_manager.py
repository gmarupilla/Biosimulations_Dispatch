""" Chart manager to manage Charts in the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch.resource_manager import ResourceManager


class ChartManager(ResourceManager):

    def _create(self, **kwargs):

        resource = super()._create(**kwargs)
        specification = kwargs.get("specification", "")
        Chart = {"specification": specification}
        resource.update((Chart))

        return resource
