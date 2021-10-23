

def run(self, tmp=None, task_vars=None):
    if (self._play_context.connection != 'local'):
        return dict(failed=True, msg=('invalid connection specified, expected connection=local, got %s' % self._play_context.connection))
    module = module_loader._load_module_source(self._task.action, module_loader.find_plugin(self._task.action))
    if (not getattr(module, 'USE_PERSISTENT_CONNECTION', False)):
        return super(ActionModule, self).run(tmp, task_vars)
    provider = self.load_provider()
    pc = copy.deepcopy(self._play_context)
    pc.network_os = 'junos'
    pc.remote_addr = (provider['host'] or self._play_context.remote_addr)
    if (self._task.action == 'junos_netconf'):
        pc.connection = 'network_cli'
        pc.port = int((provider['port'] or self._play_context.port or 22))
    else:
        pc.connection = 'netconf'
        pc.port = int((provider['port'] or self._play_context.port or 830))
    pc.remote_user = (provider['username'] or self._play_context.connection_user)
    pc.password = (provider['password'] or self._play_context.password)
    pc.private_key_file = (provider['ssh_keyfile'] or self._play_context.private_key_file)
    pc.timeout = (provider['timeout'] or self._play_context.timeout)
    display.vvv(('using connection plugin %s' % pc.connection), pc.remote_addr)
    connection = self._shared_loader_obj.connection_loader.get('persistent', pc, sys.stdin)
    socket_path = connection.run()
    display.vvvv(('socket_path: %s' % socket_path), pc.remote_addr)
    if (not socket_path):
        return {
            'failed': True,
            'msg': ('unable to open shell. Please see: ' + 'https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell'),
        }
    if (pc.connection == 'network_cli'):
        (rc, out, err) = connection.exec_command('prompt()')
        while str(out).strip().endswith(')#'):
            display.vvvv('wrong context, sending exit to device', self._play_context.remote_addr)
            connection.exec_command('exit')
            (rc, out, err) = connection.exec_command('prompt()')
    task_vars['ansible_socket'] = socket_path
    result = super(ActionModule, self).run(tmp, task_vars)
    return result
