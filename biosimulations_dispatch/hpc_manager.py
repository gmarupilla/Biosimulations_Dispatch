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
        self.allowed_biosimulators = ['COPASI', 'VCELL']
        # self.authDB = config.Config.AUTHDB
        # self.read_preference = config.Config.READ_PREFERENCE
        self.ssh, self.ftp_client = self.__setup_ssh_ftp(host=server, username=username, password=password)


    def dispatch_job(
            self, 
            simulator: str, 
            value_dict: dict, 
            sedml: str, 
            sedml_name: str, 
            sbml: str, 
            sbml_name: str,
            subscriber_id: str):
        if simulator in self.allowed_biosimulators:
            # Generate SBATCH file using value_dict
            # Create SBML using given data and name on HPC inside subscriber's simulation using simId
            # Create SEDML using given data and name on HPC inside subscriber's simulation using simId
            # Run the command to execute the simulation inside subscriber's simulation dir using simId
            return True
        else: 
            return False

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