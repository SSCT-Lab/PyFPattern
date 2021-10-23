

def _get_connection(self, variables, templar):
    '\n        Reads the connection property for the host, and returns the\n        correct connection object from the list of connection plugins\n        '
    if (self._task.delegate_to is not None):
        for i in list(variables.keys()):
            if (isinstance(i, string_types) and i.startswith('ansible_') and i.endswith('_interpreter')):
                del variables[i]
        delegated_vars = variables.get('ansible_delegated_vars', dict()).get(self._task.delegate_to, dict())
        if isinstance(delegated_vars, dict):
            for i in delegated_vars:
                if (isinstance(i, string_types) and i.startswith('ansible_') and i.endswith('_interpreter')):
                    variables[i] = delegated_vars[i]
    conn_type = self._play_context.connection
    connection = self._shared_loader_obj.connection_loader.get(conn_type, self._play_context, self._new_stdin, task_uuid=self._task._uuid, ansible_playbook_pid=to_text(os.getppid()))
    if (not connection):
        raise AnsibleError(("the connection plugin '%s' was not found" % conn_type))
    become_plugin = None
    if self._play_context.become:
        become_plugin = self._get_become(self._play_context.become_method)
    if (getattr(become_plugin, 'require_tty', False) and (not getattr(connection, 'has_tty', False))):
        raise AnsibleError(("The '%s' connection does not provide a tty which is requied for the selected become plugin: %s." % (conn_type, become_plugin.name)))
    try:
        connection.set_become_plugin(become_plugin)
    except AttributeError:
        pass
    self._play_context.set_become_plugin(become_plugin)
    self._play_context.set_attributes_from_plugin(connection)
    if any(((connection.supports_persistence and C.USE_PERSISTENT_CONNECTIONS), connection.force_persistence)):
        self._play_context.timeout = connection.get_option('persistent_command_timeout')
        display.vvvv('attempting to start connection', host=self._play_context.remote_addr)
        display.vvvv(('using connection plugin %s' % connection.transport), host=self._play_context.remote_addr)
        options = self._get_persistent_connection_options(connection, variables, templar)
        socket_path = start_connection(self._play_context, options)
        display.vvvv(('local domain socket path is %s' % socket_path), host=self._play_context.remote_addr)
        setattr(connection, '_socket_path', socket_path)
    return connection
