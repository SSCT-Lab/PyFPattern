

def run(self, tmp=None, task_vars=None):
    if (self._play_context.connection != 'local'):
        return dict(failed=True, msg=('invalid connection specified, expected connection=local, got %s' % self._play_context.connection))
    provider = self.load_provider()
    transport = (provider['transport'] or 'cli')
    display.vvvv(('connection transport is %s' % transport), self._play_context.remote_addr)
    if (transport == 'cli'):
        pc = copy.deepcopy(self._play_context)
        pc.connection = 'network_cli'
        pc.network_os = 'eos'
        pc.remote_addr = (provider['host'] or self._play_context.remote_addr)
        pc.port = (provider['port'] or self._play_context.port or 22)
        pc.remote_user = (provider['username'] or self._play_context.connection_user)
        pc.password = (provider['password'] or self._play_context.password)
        pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
        pc.timeout = (provider['timeout'] or C.PERSISTENT_COMMAND_TIMEOUT)
        pc.become = (provider['authorize'] or False)
        pc.become_pass = provider['auth_pass']
        display.vvv(('using connection plugin %s' % pc.connection), pc.remote_addr)
        connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
        socket_path = connection.run()
        display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
        if (not socket_path):
            return {
                'failed': True,
                'msg': ('unable to open shell. Please see: ' + 'https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell'),
            }
        (rc, out, err) = connection.exec_command('prompt()')
        while ('(config' in str(out)):
            display.vvvv('wrong context, sending exit to device', self._play_context.remote_addr)
            connection.exec_command('exit')
            (rc, out, err) = connection.exec_command('prompt()')
        task_vars['ansible_socket'] = socket_path
    else:
        provider['transport'] = 'eapi'
        if (provider.get('host') is None):
            provider['host'] = self._play_context.remote_addr
        if (provider.get('use_ssl') is None):
            provider['use_ssl'] = ARGS_DEFAULT_VALUE['use_ssl']
        if (provider.get('port') is None):
            default_port = (443 if provider['use_ssl'] else 80)
            provider['port'] = (self._play_context.port or default_port)
        if (provider.get('timeout') is None):
            provider['timeout'] = self._play_context.timeout
        if (provider.get('username') is None):
            provider['username'] = self._play_context.connection_user
        if (provider.get('password') is None):
            provider['password'] = self._play_context.password
        if (provider.get('authorize') is None):
            provider['authorize'] = False
        if (provider.get('validate_certs') is None):
            provider['validate_certs'] = ARGS_DEFAULT_VALUE['validate_certs']
        self._task.args['provider'] = provider
    result = super(ActionModule, self).run(tmp, task_vars)
    return result
