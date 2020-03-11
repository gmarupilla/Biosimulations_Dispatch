import os
from biosimulations_dispatch.sbatch.templates import VCellTemplate, CopasiTemplate
import paramiko
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
        if self.username is None:
            self.username = Config.HPC_USER
        if self.password is None:
            self.password = Config.HPC_PASS
        if self.server is None:
            self.server = Config.HPC_HOST
        self.allowed_biosimulators = {
            'VCELL': VCellTemplate,
            'COPASI': CopasiTemplate
        }
        self.ssh, self.ftp_client = self.__setup_ssh_ftp(host=server, username=username, password=password)

    def dispatch_job(
            self, simulator: str, 
            value_dict: dict, 
            sedml: str, 
            sedml_name: str, 
            sbml: str):
        """
        SEDML_NAME and SBML_NAME are without extensions in param
        """
        if simulator in self.allowed_biosimulators.keys():
            # Hardcoded for 1 model - 1 task sedml file
            sbml_name = 'model'

            # Generate SBATCH file using value_dict
            simulator_sbatch_instance = self.allowed_biosimulators[simulator]()

            # TODO: use query module to store sbatch inside DB
            sbatch = simulator_sbatch_instance.fill_values(value_dict)
            
            # Creating directory to store everything related to simulation
            # TODO: Store dispatch outputs/errors in DB using query module
            directory = value_dict['tempDir']
            (stdin, stdout, stderr) = self.ssh.exec_command(
                    'mkdir -p {}'.format(directory)
                )
            
            # Create sbatch file inside simultion directory
            sbatch_remote = self.ftp_client.file('{}/run.sbatch'.format(directory), 'w', -1)
            sbatch_remote.write(sbatch)
            sbatch_remote.flush()

            # Create SBML using given data and name on HPC inside subscriber's simulation using simId
            sbml_remote = self.ftp_client.file('{}/{}.xml'.format(directory, sbml_name), 'w', -1)
            sbml_remote.write(sbml)
            sbml_remote.flush()

            # Create SEDML using given data and name on HPC inside subscriber's simulation using simId
            sedml_remote = self.ftp_client.file('{}/{}.sedml'.format(directory, sedml_name), 'w', -1)
            sedml_remote.write(sedml)
            sedml_remote.flush()

            # Run the command to execute the simulation inside subscriber's simulation dir using simId
            (stdin, stdout, stderr) = self.ssh.exec_command(
                    'sbatch {}/run.sbatch'.format(directory)
                )
            return True
        else: 
            return False

    def get_output_file(self, sim_spec: dict, local_path: str):
        path = sim_spec['tempDir']
        files_path = os.path.join(path, 'out')
        # TODO: Check the Task DIR from task name when accepting more than 1 task for simulation
        task_dir = self.ftp_client.listdir(files_path)[0]
        files_path = os.path.join(files_path, task_dir)
        remote_files = self.ftp_client.listdir(files_path)
        complete_local_path = os.path.join(local_path, sim_spec['owner'], sim_spec['id'])
        for file in remote_files:
            if file.endswith('.ida') or file.endswith('.cvodeInput') or file.endswith('.xml'):
                self.ftp_client.get(
                        os.path.join(files_path, file),
                        complete_local_path
                    )
        return True

    def __setup_ssh_ftp(self, host=None, username=None, password=None):
        """Set up the SSH and FTP connections to the HPC

        Args:
            host (String, optional): The hostname of the server. Defaults the configuration
            username (String, optional): The username. Defaults to the configuration
            password (String, optional): The password. Defaults to the configuration`

        Returns:
            ssh_client, ftp_client: The SHH and FTP connections to the HPC"""

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            host,
            username=username,
            password=password
        )
        ftp_client = ssh.open_sftp()
        return ssh, ftp_client
