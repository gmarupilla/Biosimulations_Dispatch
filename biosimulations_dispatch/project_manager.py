""" Project manager to manage Projects in the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch.resource_manager import ResourceManager


class ProjectManager(ResourceManager):

    def _create(self, **kwargs):

        resource = super()._create(**kwargs)
        products = kwargs.get("products", [])
        Project = {"products": products}
        resource.update((Project))

        return resource
