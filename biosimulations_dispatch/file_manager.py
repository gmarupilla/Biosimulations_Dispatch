""" File manager to manage files with database and FTP server

:Author: Akhil Marupilla < akhilmteja@gmail.com >
:Date: 2019-11-09
:Copyright: 2019, UCONN Health
:License: MIT
"""
from biosimulations_dispatch.utils import MongoUtil
import gridfs


class FileManager(object):

    def __init__(
            self,
            username=None,
            password=None,
            host="localhost",
            authSource="admin",
            database="test",
            collection="files"):

        self.mongo_manager = MongoUtil(
            host=host,
            username=username,
            password=password,
            authSource=authSource,
            db=database,
        )

        self.client, self.db, self.collection = self.mongo_manager.con_db(
            collection)
        self.fs = gridfs.GridFS(self.db)

    ######### CREATE ###########

    def add_file(self):
        pass

    def add_file_to_db(self, file, file_name):
        return self.fs.put(file, filename=file_name)

    def add_file_to_ftp(self):
        pass

    ##########################

    ######## RETRIEVE ##########

    def get_file(self):
        pass

    def get_file_from_db_by_id(self, file_id):

        return self.fs.get(file_id)

    def get_file_from_db_by_name(self, file_name):

        return self.fs.find_one({"filename": file_name})

    def get_file_from_ftp(self):
        pass

    ############################

    ######## UPDATE ############

    def update_file(self):
        pass

    def update_file_from_db(self):
        pass

    def update_file_from_ftp(self):
        pass

    ######### DELETE #############

    def delete_file(self):
        pass

    def delete_file_from_db(self):
        pass

    def delete_file_from_ftp(self):
        pass

    ########## UTIL ##############

    def extract_archive(self):
        pass

    def get_model_from_archive(self):
        pass

    def get_simulation_from_archive(self):
        pass
