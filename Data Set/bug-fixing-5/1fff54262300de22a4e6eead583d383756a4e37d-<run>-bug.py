def run(self, tmp=None, task_vars=None):
    del tmp
    socket_path = None
    if (((self._play_context.connection == 'httpapi') or (self._task.args.get('provider', {
        
    }).get('transport') == 'nxapi')) and (self._task.action in ('nxos_file_copy', 'nxos_nxapi'))):
        return {
            'failed': True,
            'msg': ("Transport type 'nxapi' is not valid for '%s' module." % self._task.action),
        }
    if (self._task.action == 'nxos_file_copy'):
        self._task.args['host'] = self._play_context.remote_addr
        self._task.args['password'] = self._play_context.password
        if (self._play_context.connection == 'network_cli'):
            self._task.args['username'] = self._play_context.remote_user
        elif (self._play_context.connection == 'local'):
            self._task.args['username'] = self._play_context.connection_user
    if (self._task.action == 'nxos_install_os'):
        if ((C.PERSISTENT_COMMAND_TIMEOUT < 600) or (C.PERSISTENT_CONNECT_TIMEOUT < 600)):
            msg = 'PERSISTENT_COMMAND_TIMEOUT and PERSISTENT_CONNECT_TIMEOUT'
            msg += ' must be set to 600 seconds or higher when using nxos_install_os module'
            return {
                'failed': True,
                'msg': msg,
            }
    if (self._play_context.connection in ('network_cli', 'httpapi')):
        provider = self._task.args.get('provider', {
            
        })
        if any(provider.values()):
            display.warning(('provider is unnecessary when using %s and will be ignored' % self._play_context.connection))
            del self._task.args['provider']
        if self._task.args.get('transport'):
            display.warning(('transport is unnecessary when using %s and will be ignored' % self._play_context.connection))
            del self._task.args['transport']
    elif (self._play_context.connection == 'local'):
        provider = load_provider(nxos_provider_spec, self._task.args)
        transport = (provider['transport'] or 'cli')
        display.vvvv(('connection transport is %s' % transport), self._play_context.remote_addr)
        if (transport == 'cli'):
            pc = copy.deepcopy(self._play_context)
            pc.connection = 'network_cli'
            pc.network_os = 'nxos'
            pc.remote_addr = (provider['host'] or self._play_context.remote_addr)
            pc.port = int((provider['port'] or self._play_context.port or 22))
            pc.remote_user = (provider['username'] or self._play_context.connection_user)
            pc.password = (provider['password'] or self._play_context.password)
            pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
            pc.become = (provider['authorize'] or False)
            if pc.become:
                pc.become_method = 'enable'
            pc.become_pass = provider['auth_pass']
            display.vvv(('using connection plugin %s (was local)' % pc.connection), pc.remote_addr)
            connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
            command_timeout = (int(provider['timeout']) if provider['timeout'] else connection.get_option('persistent_command_timeout'))
            connection.set_options(direct={
                'persistent_command_timeout': command_timeout,
            })
            socket_path = connection.run()
            display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
            if (not socket_path):
                return {
                    'failed': True,
                    'msg': ('unable to open shell. Please see: ' + 'https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell'),
                }
            task_vars['ansible_socket'] = socket_path
        else:
            self._task.args['provider'] = ActionModule.nxapi_implementation(provider, self._play_context)
    else:
        return {
            'failed': True,
            'msg': ('Connection type %s is not valid for this module' % self._play_context.connection),
        }
    if (((self._play_context.connection == 'local') and (transport == 'cli')) or (self._play_context.connection == 'network_cli')):
        if (socket_path is None):
            socket_path = self._connection.socket_path
        conn = Connection(socket_path)
        out = conn.get_prompt()
        while to_text(out, errors='surrogate_then_replace').strip().endswith(')#'):
            display.vvvv('wrong context, sending exit to device', self._play_context.remote_addr)
            conn.send_command('exit')
            out = conn.get_prompt()
    result = super(ActionModule, self).run(task_vars=task_vars)
    return result