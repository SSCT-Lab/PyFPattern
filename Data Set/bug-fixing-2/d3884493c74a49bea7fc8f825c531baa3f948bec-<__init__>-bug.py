

def __init__(self, ssh_conn_id=None, remote_host=None, username=None, password=None, key_file=None, port=None, timeout=10, keepalive_interval=30):
    super().__init__(ssh_conn_id)
    self.ssh_conn_id = ssh_conn_id
    self.remote_host = remote_host
    self.username = username
    self.password = password
    self.key_file = key_file
    self.port = port
    self.timeout = timeout
    self.keepalive_interval = keepalive_interval
    self.compress = True
    self.no_host_key_check = True
    self.allow_host_key_change = False
    self.host_proxy = None
    self.client = None
    if (self.ssh_conn_id is not None):
        conn = self.get_connection(self.ssh_conn_id)
        if (self.username is None):
            self.username = conn.login
        if (self.password is None):
            self.password = conn.password
        if (self.remote_host is None):
            self.remote_host = conn.host
        if (self.port is None):
            self.port = conn.port
        if (conn.extra is not None):
            extra_options = conn.extra_dejson
            if ('key_file' in extra_options):
                self.key_file = extra_options.get('key_file')
            if ('timeout' in extra_options):
                self.timeout = int(extra_options['timeout'], 10)
            if (('compress' in extra_options) and (str(extra_options['compress']).lower() == 'false')):
                self.compress = False
            if (('no_host_key_check' in extra_options) and (str(extra_options['no_host_key_check']).lower() == 'false')):
                self.no_host_key_check = False
            if (('allow_host_key_change' in extra_options) and (str(extra_options['allow_host_key_change']).lower() == 'true')):
                self.allow_host_key_change = True
    if (not self.remote_host):
        raise AirflowException('Missing required param: remote_host')
    if (not self.username):
        self.log.debug("username to ssh to host: %s is not specified for connection id %s. Using system's default provided by getpass.getuser()", self.remote_host, self.ssh_conn_id)
        self.username = getpass.getuser()
    user_ssh_config_filename = os.path.expanduser('~/.ssh/config')
    if os.path.isfile(user_ssh_config_filename):
        ssh_conf = paramiko.SSHConfig()
        ssh_conf.parse(open(user_ssh_config_filename))
        host_info = ssh_conf.lookup(self.remote_host)
        if (host_info and host_info.get('proxycommand')):
            self.host_proxy = paramiko.ProxyCommand(host_info.get('proxycommand'))
        if (not (self.password or self.key_file)):
            if (host_info and host_info.get('identityfile')):
                self.key_file = host_info.get('identityfile')[0]
    self.port = (self.port or SSH_PORT)
