def _connect(self):
    '\n        Connects to the remote device and starts the terminal\n        '
    if self.connected:
        return
    p = connection_loader.get('paramiko', self._play_context, '/dev/null')
    p.set_options(direct={
        'look_for_keys': bool((self._play_context.password and (not self._play_context.private_key_file))),
    })
    p.force_persistence = self.force_persistence
    ssh = p._connect()
    display.vvvv('ssh connection done, setting terminal', host=self._play_context.remote_addr)
    self._ssh_shell = ssh.ssh.invoke_shell()
    self._ssh_shell.settimeout(self._play_context.timeout)
    network_os = self._play_context.network_os
    if (not network_os):
        raise AnsibleConnectionFailure('Unable to automatically determine host network os. Please manually configure ansible_network_os value for this host')
    self._terminal = terminal_loader.get(network_os, self)
    if (not self._terminal):
        raise AnsibleConnectionFailure(('network os %s is not supported' % network_os))
    display.vvvv(('loaded terminal plugin for network_os %s' % network_os), host=self._play_context.remote_addr)
    self._cliconf = cliconf_loader.get(network_os, self)
    if self._cliconf:
        display.vvvv(('loaded cliconf plugin for network_os %s' % network_os), host=self._play_context.remote_addr)
    else:
        display.vvvv(('unable to load cliconf for network_os %s' % network_os))
    self.receive()
    display.vvvv('firing event: on_open_shell()', host=self._play_context.remote_addr)
    self._terminal.on_open_shell()
    if (self._play_context.become and (self._play_context.become_method == 'enable')):
        display.vvvv('firing event: on_authorize', host=self._play_context.remote_addr)
        auth_pass = self._play_context.become_pass
        self._terminal.on_authorize(passwd=auth_pass)
    display.vvvv('ssh connection has completed successfully', host=self._play_context.remote_addr)
    self._connected = True
    return self