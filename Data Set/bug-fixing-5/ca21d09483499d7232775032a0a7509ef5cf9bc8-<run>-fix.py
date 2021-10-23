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
        pc.remote_user = (provider['username'] or self._play_context.connection_user)
        pc.password = (provider['password'] or self._play_context.password)
        pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
        pc.timeout = (provider['timeout'] or self._play_context.timeout)
        pc.become = (provider['authorize'] or False)
        pc.become_pass = provider['auth_pass']
        connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
        socket_path = self._get_socket_path(pc)
        display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
        if (not os.path.exists(socket_path)):
            display.vvvv('calling open_shell()', pc.remote_addr)
            (rc, out, err) = connection.exec_command('open_shell()')
            if (not (rc == 0)):
                return {
                    'failed': True,
                    'msg': 'unable to open shell',
                }
        else:
            (rc, out, err) = connection.exec_command('prompt()')
            while str(out).strip().endswith(')#'):
                display.debug('wrong context, sending exit to device', self._play_context.remote_addr)
                connection.exec_command('exit')
                (rc, out, err) = connection.exec_command('prompt()')
        task_vars['ansible_socket'] = socket_path
    else:
        provider_arg = {
            'transport': 'eapi',
            'host': (provider.get('host') or self._play_context.remote_addr),
            'port': provider.get('port'),
            'username': (provider.get('username') or self._play_context.connection_user),
            'password': (provider.get('password') or self._play_context.password),
            'authorize': (provider.get('authorize') or False),
            'auth_pass': provider.get('auth_pass'),
            'timeout': (provider.get('timeout') or self._play_context.timeout),
            'use_ssl': (task_vars.get('eapi_use_ssl') or False),
            'validate_certs': (task_vars.get('eapi_validate_certs') or True),
        }
        self._task.args['provider'] = provider_arg
    if (self._play_context.become_method == 'enable'):
        self._play_context.become = False
        self._play_context.become_method = None
    return super(ActionModule, self).run(tmp, task_vars)