""" Model manager to manage models in the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch.resource_manager import ResourceManager


class ModelManager(ResourceManager):

    def _create(self, **kwargs):

        resource = super()._create(**kwargs)

        parameters = kwargs.get("parameters", [])
        model_file = kwargs.get("file", "")
        framework = kwargs.get("framework", [])
        simulator_format = kwargs.get("format", [])
        taxon = kwargs.get("taxon", {"id": 0, "name": ""})
        model = {
            "parameters": parameters,
            "file": model_file,
            "framework": framework,
            "format": simulator_format,
            "taxon": taxon}

        resource.update((model))

        return resource
