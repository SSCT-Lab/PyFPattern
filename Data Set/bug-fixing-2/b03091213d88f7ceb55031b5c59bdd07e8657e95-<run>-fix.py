

def run(self, tmp=None, task_vars=None):
    socket_path = None
    self.play_context = copy.deepcopy(self._play_context)
    self.results = super(ActionModule, self).run(task_vars=task_vars)
    if (self.play_context.connection != 'network_cli'):
        self.results['failed'] = True
        self.results['msg'] = 'Connection type must be <network_cli>'
        return self.results
    self.playvals = self.process_playbook_values()
    file_pull = self.playvals['file_pull']
    self.check_library_dependencies(file_pull)
    if (socket_path is None):
        socket_path = self._connection.socket_path
    self.conn = Connection(socket_path)
    self.conn.get_capabilities()
    self.socket_timeout = self.conn.get_option('persistent_command_timeout')
    self.results['transfer_status'] = 'No Transfer'
    self.results['file_system'] = self.playvals['file_system']
    if file_pull:
        self.file_pull()
    else:
        self.file_push()
    return self.results
