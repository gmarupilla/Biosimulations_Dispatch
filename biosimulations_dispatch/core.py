""" The core file for the dispatch package, which connects to the database

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
"""
from biosimulations_dispatch import config
from biosimulations_dispatch import user_manager
from biosimulations_dispatch import simulation_manager
from biosimulations_dispatch import model_manager
from biosimulations_dispatch import project_manager
from biosimulations_dispatch import chart_manager
from biosimulations_dispatch import visualization_manager
from biosimulations_dispatch import file_manager


class DBManager:
    def __init__(
            self,
            database=None,
            username=None,
            password=None,
            server=None,
            authSource="admin"):
        self.username = username
        self.password = password
        self.server = server
        self.database = database
        self.authSource = authSource
        if(not self.username):
            self.username = config.Config.USERNAME
        if (not self.password):
            self.password = config.Config.PASSWORD
        if (not self.server):
            self.server = config.Config.SERVER
        if(not database):
            self.database = config.Config.DATABASE
        # self.authDB = config.Config.AUTHDB
        # self.read_preference = config.Config.READ_PREFERENCE

    def user_manager(self):
        return user_manager.UserManager(
            username=self.username,
            password=self.password,
            host=self.server,
            database=self.database,
            collection="user")

    def simulation_manager(self):
        return simulation_manager.SimulationManager(
            username=self.username,
            password=self.password,
            host=self.server,
            database=self.database,
            authSource=self.authSource,
            collection="simulations")

    def model_manager(self):
        return model_manager.ModelManager(
            username=self.username,
            password=self.password,
            host=self.server,
            database=self.database,
            authSource=self.authSource,
            collection="models")

    def project_manager(self):
        return project_manager.ProjectManager(
            username=self.username,
            password=self.password,
            host=self.server,
            database=self.database,
            authSource=self.authSource,
            collection="projects")

    def chart_manager(self):
        return chart_manager.ChartManager(
            username=self.username,
            password=self.password,
            host=self.server,
            database=self.database,
            authSource=self.authSource,
            collection="charts")

    def visualization_manager(self):
        return visualization_manager.VisualizationManager(
            username=self.username,
            password=self.password,
            host=self.server,
            database=self.database,
            authSource=self.authSource,
            collection="visualizations")

    def file_manager(self):
        return file_manager.FileManager(
            username=self.username,
            password=self.password,
            host=self.server,
            database=self.database)


if __name__ == "__main__":
    dbm = DBManager()
    um = dbm.user_manager()
