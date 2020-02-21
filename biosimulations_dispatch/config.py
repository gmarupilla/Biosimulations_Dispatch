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
    HPC_HOST = os.environ.get('HPC_HOST')
    HPC_USER = os.environ.get('HPC_USER')
    HPC_PASS = os.environ.get('HPC_PASS')
    JOBHOOK_URL = '{}/jobhook'.format(os.getenv('JOBHOOK_HOST'))
