def _connect(self):
    'Connections to the device and sets the terminal type'
    super(Connection, self)._connect()
    display.debug('starting network_cli._connect()')
    network_os = self._play_context.network_os
    if (not network_os):
        for cls in terminal_loader.all(class_only=True):
            try:
                network_os = cls.guess_network_os(self.ssh)
                if network_os:
                    break
            except:
                raise AnsibleConnectionFailure('Unable to automatically determine host network os. Please manually configure ansible_network_os value for this host')
    if (not network_os):
        raise AnsibleConnectionFailure('Unable to automatically determine host network os. Please manually configure ansible_network_os value for this host')
    self._terminal = terminal_loader.get(network_os, self)
    if (not self._terminal):
        raise AnsibleConnectionFailure(('network os %s is not supported' % network_os))
    self._connected = True