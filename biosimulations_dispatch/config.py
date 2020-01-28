""" Config

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, Karr Lab
:License: MIT
Contains the configuration for the dispatch module to connect to the database"""
from dotenv import load_dotenv
from pathlib import Path, PurePath
import os

home_path = str(PurePath(str(Path.home()), 'crbm.env'))
if os.path.exists(home_path):
    dotenv_path = home_path
    load_dotenv(dotenv_path)


class Config(object):
    PRODUCTION = os.getenv("PRODUCTION", False)
    USERNAME = os.getenv("MONGO_USERNAME")
    PASSWORD = os.getenv("MONGO_PASSWORD")
    SERVER = os.getenv("MONGO_SERVER")
    PORT = os.getenv("MONGO_PORT", None)
    DATABASE = os.getenv("MONGO_DATABASE", "Test_DB")
    # Below are not needed for now, may be if we start to self manage repl sets
    REPLSET = os.getenv("MONGO_REPL")
    AUTHDB = os.getenv("MONGO_AUTHDB")
    SESSION_KEY = os.getenv("FLASK_SESSION_KEY")
    READ_PREFERENCE = os.getenv("READ_PREFERENCE")


