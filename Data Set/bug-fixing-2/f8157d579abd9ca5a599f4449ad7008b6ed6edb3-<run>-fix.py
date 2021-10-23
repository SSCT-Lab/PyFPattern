

def run(self, tmp=None, task_vars=None):
    if (self._play_context.connection != 'local'):
        return dict(failed=True, msg=('invalid connection specified, expected connection=local, got %s' % self._play_context.connection))
    provider = self.load_provider()
    transport = (provider['transport'] or 'cli')
    display.vvvv(('connection transport is %s' % transport), self._play_context.remote_addr)
    if (transport == 'cli'):
        pc = copy.deepcopy(self._play_context)
        pc.connection = 'network_cli'
        pc.network_os = 'nxos'
        pc.port = (provider['port'] or self._play_context.port or 22)
        pc.remote_user = (provider['username'] or self._play_context.connection_user)
        pc.password = (provider['password'] or self._play_context.password)
        pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
        pc.timeout = (provider['timeout'] or self._play_context.timeout)
        connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
        socket_path = self._get_socket_path(pc)
        display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
        if (not os.path.exists(socket_path)):
            (rc, out, err) = connection.exec_command('open_shell()')
            display.vvvv(('open_shell() returned %s %s %s' % (rc, out, err)))
            if (rc != 0):
                return {
                    'failed': True,
                    'msg': 'unable to open shell',
                    'rc': rc,
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
            'host': self._play_context.remote_addr,
            'port': provider.get('port'),
            'username': (provider.get('username') or self._play_context.connection_user),
            'password': (provider.get('password') or self._play_context.password),
            'timeout': (provider.get('timeout') or self._play_context.timeout),
            'use_ssl': (task_vars.get('nxapi_use_ssl') or False),
            'validate_certs': (task_vars.get('nxapi_validate_certs') or True),
        }
        self._task.args['provider'] = provider_arg
    if ((self._task.args.get('transport') is None) and (self._task.args.get('provider').get('transport') is None)):
        self._task.args['transport'] = 'cli'
    return super(ActionModule, self).run(tmp, task_vars)
