""" The core file for the dispatch package, which connects to the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch.config import Config


class HPCManager:
    def __init__(
            self,
            username=None,
            password=None,
            server=None):
        self.username = username
        self.password = password
        self.server = server
        if not self.username:
            self.username = Config.USERNAME
        if not self.password:
            self.password = Config.PASSWORD
        if not self.server:
            self.server = Config.SERVER
        # self.authDB = config.Config.AUTHDB
        # self.read_preference = config.Config.READ_PREFERENCE

    def user_manager(self):
        return self.user_manager.UserManager(
            username=self.username,
            password=self.password,
            host=self.server,
            collection="user")

    def simulation_manager(self):
        return self.simulation_manager.SimulationManager(
            username=self.username,
            password=self.password,
            host=self.server,
            collection="simulations")

    def model_manager(self):
        return self.model_manager.ModelManager(
            username=self.username,
            password=self.password,
            host=self.server,
            collection="models")


if __name__ == "__main__":
    hpc = HPCManager()
    hm = hpc.user_manager()
