""" The core file which triggers the job dispatch

:Author: Akhil Teja < akhilmteja@gmail.com >
:Date: 2020-02-03
:Copyright: UCONN Health
:License: MIT
"""

from biosimulations_dispatch import HPCManager, Config


if __name__ == "__main__":
    hpc = HPCManager(username=Config.HPC_USER, password=Config.HPC_PASS, server=Config.HPC_HOST)
