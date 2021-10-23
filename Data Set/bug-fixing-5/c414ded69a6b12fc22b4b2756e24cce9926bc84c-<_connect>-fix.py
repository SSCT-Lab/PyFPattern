def _connect(self):
    super(Connection, self)._connect()
    network_os = self._play_context.network_os
    if (not network_os):
        for cls in terminal_loader.all(class_only=True):
            network_os = cls.guess_network_os(self.ssh)
            if network_os:
                break
    if (not network_os):
        raise AnsibleConnectionFailure('unable to determine device network os.  Please configure ansible_network_os value')
    self._terminal = terminal_loader.get(network_os, self)
    if (not self._terminal):
        raise AnsibleConnectionFailure(('network os %s is not supported' % network_os))
    return (0, 'connected', '')