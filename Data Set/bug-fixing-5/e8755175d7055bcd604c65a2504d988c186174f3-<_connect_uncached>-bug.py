def _connect_uncached(self):
    ' activates the connection object '
    if (not HAVE_PARAMIKO):
        raise AnsibleError('paramiko is not installed')
    port = (self._play_context.port or 22)
    display.vvv(('ESTABLISH CONNECTION FOR USER: %s on PORT %s TO %s' % (self._play_context.remote_user, port, self._play_context.remote_addr)), host=self._play_context.remote_addr)
    ssh = paramiko.SSHClient()
    self.keyfile = os.path.expanduser('~/.ssh/known_hosts')
    if self.get_option('host_key_checking'):
        for ssh_known_hosts in ('/etc/ssh/ssh_known_hosts', '/etc/openssh/ssh_known_hosts'):
            try:
                ssh.load_system_host_keys(ssh_known_hosts)
                break
            except IOError:
                pass
        ssh.load_system_host_keys()
    sock_kwarg = self._parse_proxy_command(port)
    ssh.set_missing_host_key_policy(MyAddPolicy(self._new_stdin, self))
    allow_agent = True
    if (self._play_context.password is not None):
        allow_agent = False
    try:
        key_filename = None
        if self._play_context.private_key_file:
            key_filename = os.path.expanduser(self._play_context.private_key_file)
        ssh.connect(self._play_context.remote_addr, username=self._play_context.remote_user, allow_agent=allow_agent, look_for_keys=self.get_option('look_for_keys'), key_filename=key_filename, password=self._play_context.password, timeout=self._play_context.timeout, port=port, **sock_kwarg)
    except paramiko.ssh_exception.BadHostKeyException as e:
        raise AnsibleConnectionFailure(('host key mismatch for %s' % e.hostname))
    except Exception as e:
        msg = str(e)
        if ('PID check failed' in msg):
            raise AnsibleError('paramiko version issue, please upgrade paramiko on the machine running ansible')
        elif ('Private key file is encrypted' in msg):
            msg = ('ssh %s@%s:%s : %s\nTo connect as a different user, use -u <username>.' % (self._play_context.remote_user, self._play_context.remote_addr, port, msg))
            raise AnsibleConnectionFailure(msg)
        else:
            raise AnsibleConnectionFailure(msg)
    return ssh