def open(self, host, port=22, username=None, password=None, timeout=10, key_filename=None, pkey=None, look_for_keys=None, allow_agent=False, key_policy='loose'):
    self.ssh = paramiko.SSHClient()
    if (key_policy != 'ignore'):
        self.ssh.load_system_host_keys()
        try:
            self.ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            pass
    if (key_policy == 'strict'):
        self.ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
    else:
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if (not look_for_keys):
        look_for_keys = (password is None)
    try:
        self.ssh.connect(host, port=port, username=username, password=password, timeout=timeout, look_for_keys=look_for_keys, pkey=pkey, key_filename=key_filename, allow_agent=allow_agent)
        self.shell = self.ssh.invoke_shell()
        self.shell.settimeout(timeout)
    except socket.gaierror:
        raise ShellError('unable to resolve host name')
    except AuthenticationException:
        raise ShellError('Unable to authenticate to remote device')
    except socket.error:
        exc = get_exception()
        if (exc.errno == 60):
            raise ShellError('timeout trying to connect to host')
        raise
    if self.kickstart:
        self.shell.sendall('\n')
    self.receive()