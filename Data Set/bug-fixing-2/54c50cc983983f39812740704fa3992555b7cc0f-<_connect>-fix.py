

def _connect(self):
    super(Connection, self)._connect()
    display.display('ssh connection done, stating ncclient', log_only=True)
    self.allow_agent = True
    if (self._play_context.password is not None):
        self.allow_agent = False
    self.key_filename = None
    if self._play_context.private_key_file:
        self.key_filename = os.path.expanduser(self._play_context.private_key_file)
    network_os = self._play_context.network_os
    if (not network_os):
        for cls in netconf_loader.all(class_only=True):
            network_os = cls.guess_network_os(self)
            if network_os:
                display.display(('discovered network_os %s' % network_os), log_only=True)
    if (not network_os):
        raise AnsibleConnectionFailure('Unable to automatically determine host network os. Please ansible_network_os value')
    ssh_config = os.getenv('ANSIBLE_NETCONF_SSH_CONFIG', False)
    if (ssh_config == 'True'):
        ssh_config = True
    try:
        self._manager = manager.connect(host=self._play_context.remote_addr, port=(self._play_context.port or 830), username=self._play_context.remote_user, password=self._play_context.password, key_filename=str(self.key_filename), hostkey_verify=C.HOST_KEY_CHECKING, look_for_keys=C.PARAMIKO_LOOK_FOR_KEYS, allow_agent=self.allow_agent, timeout=self._play_context.timeout, device_params={
            'name': network_os,
        }, ssh_config=ssh_config)
    except SSHUnknownHostError as exc:
        raise AnsibleConnectionFailure(str(exc))
    if (not self._manager.connected):
        return (1, b'', b'not connected')
    display.display('ncclient manager object created successfully', log_only=True)
    self._connected = True
    self._netconf = netconf_loader.get(network_os, self)
    if self._netconf:
        self._rpc.add(self._netconf)
        display.display(('loaded netconf plugin for network_os %s' % network_os), log_only=True)
    else:
        display.display(('unable to load netconf for network_os %s' % network_os))
    return (0, to_bytes(self._manager.session_id, errors='surrogate_or_strict'), b'')
