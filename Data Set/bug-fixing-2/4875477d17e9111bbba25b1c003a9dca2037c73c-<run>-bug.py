

def run(self, tmp=None, task_vars=None):
    del tmp
    module = module_loader._load_module_source(self._task.action, module_loader.find_plugin(self._task.action))
    if (not getattr(module, 'USE_PERSISTENT_CONNECTION', False)):
        return super(ActionModule, self).run(task_vars=task_vars)
    socket_path = None
    if (self._play_context.connection == 'local'):
        provider = load_provider(junos_provider_spec, self._task.args)
        pc = copy.deepcopy(self._play_context)
        pc.network_os = 'junos'
        pc.remote_addr = (provider['host'] or self._play_context.remote_addr)
        if (((provider['transport'] == 'cli') and (self._task.action not in CLI_SUPPORTED_MODULES)) or ((provider['transport'] == 'netconf') and (self._task.action == 'junos_netconf'))):
            return {
                'failed': True,
                'msg': ("Transport type '%s' is not valid for '%s' module. Please see http://docs.ansible.com/ansible/latest/network/user_guide/platform_junos.html" % (provider['transport'], self._task.action)),
            }
        if ((self._task.action == 'junos_netconf') or ((provider['transport'] == 'cli') and (self._task.action == 'junos_command'))):
            pc.connection = 'network_cli'
            pc.port = int((provider['port'] or self._play_context.port or 22))
        else:
            pc.connection = 'netconf'
            pc.port = int((provider['port'] or self._play_context.port or 830))
        pc.remote_user = (provider['username'] or self._play_context.connection_user)
        pc.password = (provider['password'] or self._play_context.password)
        pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
        pc.timeout = int((provider['timeout'] or C.PERSISTENT_COMMAND_TIMEOUT))
        display.vvv(('using connection plugin %s (was local)' % pc.connection), pc.remote_addr)
        connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
        socket_path = connection.run()
        display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
        if (not socket_path):
            return {
                'failed': True,
                'msg': ('unable to open shell. Please see: ' + 'https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell'),
            }
        task_vars['ansible_socket'] = socket_path
    elif (self._play_context.connection in ('netconf', 'network_cli')):
        provider = self._task.args.get('provider', {
            
        })
        if any(provider.values()):
            display.warning(('provider is unnecessary when using connection=%s and will be ignored' % self._play_context.connection))
        if ((self._play_context.connection == 'network_cli') and (self._task.action not in CLI_SUPPORTED_MODULES)):
            return {
                'failed': True,
                'msg': ("Connection type '%s' is not valid for '%s' module. Please see http://docs.ansible.com/ansible/latest/network/user_guide/platform_junos.html" % (self._play_context.connection, self._task.action)),
            }
    if (((self._play_context.connection == 'local') and (pc.connection == 'network_cli')) or (self._play_context.connection == 'network_cli')):
        if (socket_path is None):
            socket_path = self._connection.socket_path
        conn = Connection(socket_path)
        out = conn.get_prompt()
        while to_text(out, errors='surrogate_then_replace').strip().endswith('#'):
            display.vvvv('wrong context, sending exit to device', self._play_context.remote_addr)
            conn.send_command('exit')
            out = conn.get_prompt()
    result = super(ActionModule, self).run(None, task_vars)
    return result
