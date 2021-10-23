

def run(self, tmp=None, task_vars=None):
    if (self._play_context.connection == 'local'):
        provider = load_provider(sros_provider_spec, self._task.args)
        pc = copy.deepcopy(self._play_context)
        pc.connection = 'network_cli'
        pc.network_os = 'sros'
        pc.remote_addr = (provider['host'] or self._play_context.remote_addr)
        pc.port = int((provider['port'] or self._play_context.port or 22))
        pc.remote_user = (provider['username'] or self._play_context.connection_user)
        pc.password = (provider['password'] or self._play_context.password)
        pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
        pc.timeout = int((provider['timeout'] or C.PERSISTENT_COMMAND_TIMEOUT))
        display.vvv(('using connection plugin %s' % pc.connection), pc.remote_addr)
        connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
        socket_path = connection.run()
        display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
        if (not socket_path):
            return {
                'failed': True,
                'msg': ('unable to open shell. Please see: ' + 'https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell'),
            }
        task_vars['ansible_socket'] = socket_path
    result = super(ActionModule, self).run(tmp, task_vars)
    return result
