def _connect(self):
    super(Connection, self)._connect()
    display.display('ssh connection done, starting ncclient', log_only=True)
    allow_agent = True
    if (self._play_context.password is not None):
        allow_agent = False
    setattr(self._play_context, 'allow_agent', allow_agent)
    key_filename = None
    if self._play_context.private_key_file:
        key_filename = os.path.expanduser(self._play_context.private_key_file)
    network_os = self._play_context.network_os
    if (not network_os):
        for cls in netconf_loader.all(class_only=True):
            network_os = cls.guess_network_os(self)
            if network_os:
                display.display(('discovered network_os %s' % network_os), log_only=True)
    device_params = {
        'name': (NETWORK_OS_DEVICE_PARAM_MAP.get(network_os) or network_os or 'default'),
    }
    ssh_config = os.getenv('ANSIBLE_NETCONF_SSH_CONFIG', False)
    if (ssh_config in BOOLEANS_TRUE):
        ssh_config = True
    else:
        ssh_config = None
    try:
        self._manager = manager.connect(host=self._play_context.remote_addr, port=(self._play_context.port or 830), username=self._play_context.remote_user, password=self._play_context.password, key_filename=str(key_filename), hostkey_verify=C.HOST_KEY_CHECKING, look_for_keys=C.PARAMIKO_LOOK_FOR_KEYS, device_params=device_params, allow_agent=self._play_context.allow_agent, timeout=self._play_context.timeout, ssh_config=ssh_config)
    except SSHUnknownHostError as exc:
        raise AnsibleConnectionFailure(str(exc))
    except ImportError as exc:
        raise AnsibleError('connection=netconf is not supported on {0}'.format(network_os))
    if (not self._manager.connected):
        return (1, b'', b'not connected')
    display.display('ncclient manager object created successfully', log_only=True)
    self._connected = True
    self._netconf = netconf_loader.get(network_os, self)
    if self._netconf:
        display.display(('loaded netconf plugin for network_os %s' % network_os), log_only=True)
    else:
        self._netconf = netconf_loader.get('default', self)
        display.display(('unable to load netconf plugin for network_os %s, falling back to default plugin' % network_os))
    return (0, to_bytes(self._manager.session_id, errors='surrogate_or_strict'), b'')