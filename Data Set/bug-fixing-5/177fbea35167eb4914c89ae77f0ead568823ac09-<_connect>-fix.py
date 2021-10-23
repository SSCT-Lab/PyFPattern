def _connect(self):
    super(Connection, self)._connect()
    display.display('ssh connection done, starting ncclient', log_only=True)
    allow_agent = True
    if (self._play_context.password is not None):
        allow_agent = False
    setattr(self._play_context, 'allow_agent', allow_agent)
    self.key_filename = (self._play_context.private_key_file or self.get_option('private_key_file'))
    if self.key_filename:
        self.key_filename = str(os.path.expanduser(self.key_filename))
    if (self._network_os == 'default'):
        for cls in netconf_loader.all(class_only=True):
            network_os = cls.guess_network_os(self)
            if network_os:
                display.display(('discovered network_os %s' % network_os), log_only=True)
                self._network_os = network_os
    device_params = {
        'name': (NETWORK_OS_DEVICE_PARAM_MAP.get(self._network_os) or self._network_os),
    }
    ssh_config = self.get_option('netconf_ssh_config')
    if (ssh_config in BOOLEANS_TRUE):
        ssh_config = True
    elif (ssh_config in BOOLEANS_FALSE):
        ssh_config = None
    try:
        self._manager = manager.connect(host=self._play_context.remote_addr, port=(self._play_context.port or 830), username=self._play_context.remote_user, password=self._play_context.password, key_filename=self.key_filename, hostkey_verify=self.get_option('host_key_checking'), look_for_keys=self.get_option('look_for_keys'), device_params=device_params, allow_agent=self._play_context.allow_agent, timeout=self._play_context.timeout, ssh_config=ssh_config)
    except SSHUnknownHostError as exc:
        raise AnsibleConnectionFailure(str(exc))
    except ImportError as exc:
        raise AnsibleError('connection=netconf is not supported on {0}'.format(self._network_os))
    if (not self._manager.connected):
        return (1, b'', b'not connected')
    display.display('ncclient manager object created successfully', log_only=True)
    self._connected = True
    netconf = netconf_loader.get(self._network_os, self)
    if netconf:
        display.display(('loaded netconf plugin for network_os %s' % self._network_os), log_only=True)
    else:
        netconf = netconf_loader.get('default', self)
        display.display(('unable to load netconf plugin for network_os %s, falling back to default plugin' % self._network_os))
    self._implementation_plugins.append(netconf)
    super(Connection, self)._connect()
    return (0, to_bytes(self._manager.session_id, errors='surrogate_or_strict'), b'')