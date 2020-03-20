""" Config

:Author: Akhil Marupilla < akhilmteja@gmail.com >
:Date: 2019-11-07
:Copyright: 2019, UConn Health
:License: MIT
Contains the configuration for the dispatch module to connect UConn Computer cluster(HPC) via the Service User"""

import os
from dotenv import load_dotenv

if os.getenv('HPC_HOST') is None:    
    from dotenv import load_dotenv
    load_dotenv()


class Config(object):
    PRODUCTION = os.getenv("PRODUCTION", False)
    HPC_HOST = os.environ.get('HPC_HOST')
    HPC_USER = os.environ.get('HPC_USER')
    HPC_PASS = os.environ.get('HPC_PASS')
    HPC_SFTP_HOST = os.environ.get('HPC_SFTP_HOST')
    JOBHOOK_URL = '{}/jobhook'.format(os.getenv('JOBHOOK_HOST'))
    ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN')
    TEMP_DIR = os.environ.get('TEMP_DIR')
