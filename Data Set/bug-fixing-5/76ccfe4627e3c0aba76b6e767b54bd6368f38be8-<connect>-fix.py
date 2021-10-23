def connect(self, params, kickstart=True):
    host = params['host']
    port = (params.get('port') or 22)
    username = params['username']
    password = params.get('password')
    key_file = params.get('ssh_keyfile')
    timeout = (params['timeout'] or 10)
    try:
        self.shell = Shell(kickstart=kickstart, prompts_re=self.CLI_PROMPTS_RE, errors_re=self.CLI_ERRORS_RE, timeout=timeout)
        self.shell.open(host, port=port, username=username, password=password, key_filename=key_file)
    except ShellError:
        exc = get_exception()
        raise NetworkError(msg=('failed to connect to %s:%s' % (host, port)), exc=to_native(exc))
    self._connected = True