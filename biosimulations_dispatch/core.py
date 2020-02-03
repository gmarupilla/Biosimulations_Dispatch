""" The core file which triggers the job dispatch

:Author: Akhil Teja < akhilmteja@gmail.com >
:Date: 2020-02-03
:Copyright: UCONN Health
:License: MIT
"""

from .hpc_manager import HPCManager
from .config import Config



if __name__ == "__main__":
    hpc = HPCManager(username=Config.HPC_USER, password=Config.HPC_PASS, server=Config.HPC_HOST)
