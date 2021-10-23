

def run(self, tmp=None, task_vars=None):
    socket_path = None
    if (self._play_context.connection == 'local'):
        provider = load_provider(iosxr_provider_spec, self._task.args)
        pc = copy.deepcopy(self._play_context)
        pc.connection = 'network_cli'
        pc.network_os = 'iosxr'
        pc.remote_addr = (provider['host'] or self._play_context.remote_addr)
        pc.port = int((provider['port'] or self._play_context.port or 22))
        pc.remote_user = (provider['username'] or self._play_context.connection_user)
        pc.password = (provider['password'] or self._play_context.password)
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
    if (socket_path is None):
        socket_path = self._connection.socket_path
    conn = Connection(socket_path)
    out = conn.get_prompt()
    while to_text(out, errors='surrogate_then_replace').strip().endswith(')#'):
        display.vvvv('wrong context, sending exit to device', self._play_context.remote_addr)
        conn.send_command('abort')
        out = conn.get_prompt()
    result = super(ActionModule, self).run(tmp, task_vars)
    return result
