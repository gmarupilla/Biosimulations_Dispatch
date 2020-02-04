""" Template class for copasi sbatch file
:Author: Akhil Marupilla < akhilmteja@gmail.com >
:Date: 2019-12-06
:Copyright: 2019, UCONN Health
:License: MIT
"""

template_string = \
'''#!/bin/bash
#SBATCH --job-name=test
#SBATCH --output={simulation_id}.output
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=1000

echo "Job ID: $SLURM_JOB_ID running on"
echo "Job Owner: $SLURM_JOB_UID "

export MODULEPATH=/isg/shared/modulefiles:/tgcapps/modulefiles

source /usr/share/Modules/init/bash

module load singularity/3.1.1

TMPDIR={temp_dir}
echo "using TMPDIR=$TMPDIR"
if [ ! -e $TMPDIR ]; then mkdir -p $TMPDIR ; fi

echo "job running on host `hostname -f`"

echo "id is $SLURM_JOB_ID"

echo "bash version is `bash --version`"
date

echo ENVIRONMENT
env

localSingularityImage="/home/CAM/crbmapi/copasi_latest.img"

# TODO: Update COPASI SBATCH Template
command="SINGULARITYENV_SIM_ID={simulation_id}  SINGULARITYENV_JOB_ID=$SLURM_JOB_UID   SINGULARITYENV_JOBHOOK_URL={jobhook_url} singularity run --bind $TMPDIR:/usr/local/app/copasi/simulation --pwd=/app $localSingularityImage"
echo $command

eval $command'''


class CopasiTemplate:
    def __init__(self):
        self.template_string = template_string
        self.key_list = ['simulation_id', 'temp_dir', 'jobhook_url']

    def fill_values(self, value_dict: dict):
        return self.template_string.format(**value_dict)