""" simulation_manager to manage simulations on the datbase

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch.resource_manager import ResourceManager
from .utils import parseTime


class SimulationManager(ResourceManager):

    def _create(self, **kwargs):

        resource = super()._create(**kwargs)
        model = kwargs.get("model")
        simulator_format = kwargs.get("format", {})
        model_parameter_changes = kwargs.get("modelParameterChanges", [])
        start_time = kwargs.get("startTime")
        if (start_time):
            start_time = parseTime(start_time)
        end_time = kwargs.get("endTime")
        if(end_time):
            end_time = parseTime(end_time)
        length = kwargs.get("length")
        wall_time = kwargs.get('wallTime')
        out_log = kwargs.get("outLog")
        err_log = kwargs.get("errLog")
        algorithm = kwargs.get("algorithm", {})
        algorithm_param_changes = model_parameter_changes = kwargs.get(
            "algorithmParameterChanges", [])
        simulator = kwargs.get("simulator", {})
        num_time_poins = kwargs.get("numTimePoints", 0)
        status = kwargs.get("status", "queued")

        simulation = {
            "model": model,
            "simulatorFormat": simulator_format,
            "modelParameterChanges": model_parameter_changes,
            "startTime": start_time,
            "endTime": end_time,
            "length": length,
            "wallTime": wall_time,
            "outLog": out_log,
            "errLog": err_log,
            "algorithm": algorithm,
            "algorithmParameterChanges": algorithm_param_changes,
            "simulator": simulator,
            "numTimePoints": num_time_poins,
            "status": status,
        }

        resource.update((simulation))

        return resource
