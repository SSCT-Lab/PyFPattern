

def _connect(self):
    if (not HAS_NCCLIENT):
        raise AnsibleError(('The required "ncclient" python library is required to use the netconf connection type: %s.\nPlease run pip install ncclient' % to_native(NCCLIENT_IMP_ERR)))
    self.queue_message('log', 'ssh connection done, starting ncclient')
    allow_agent = True
    if (self._play_context.password is not None):
        allow_agent = False
    setattr(self._play_context, 'allow_agent', allow_agent)
    self.key_filename = (self._play_context.private_key_file or self.get_option('private_key_file'))
    if self.key_filename:
        self.key_filename = str(os.path.expanduser(self.key_filename))
    self._ssh_config = self.get_option('netconf_ssh_config')
    if (self._ssh_config in BOOLEANS_TRUE):
        self._ssh_config = True
    elif (self._ssh_config in BOOLEANS_FALSE):
        self._ssh_config = None
    if (self._network_os == 'auto'):
        for cls in netconf_loader.all(class_only=True):
            network_os = cls.guess_network_os(self)
            if network_os:
                self.queue_message('vvv', ('discovered network_os %s' % network_os))
                self._network_os = network_os
    if (self._network_os == 'auto'):
        self.queue_message('vvv', 'Unable to discover network_os. Falling back to default.')
        self._network_os = 'default'
    device_params = {
        'name': (NETWORK_OS_DEVICE_PARAM_MAP.get(self._network_os) or self._network_os),
    }
    try:
        port = (self._play_context.port or 830)
        self.queue_message('vvv', ('ESTABLISH NETCONF SSH CONNECTION FOR USER: %s on PORT %s TO %s WITH SSH_CONFIG = %s' % (self._play_context.remote_user, port, self._play_context.remote_addr, self._ssh_config)))
        self._manager = manager.connect(host=self._play_context.remote_addr, port=port, username=self._play_context.remote_user, password=self._play_context.password, key_filename=self.key_filename, hostkey_verify=self.get_option('host_key_checking'), look_for_keys=self.get_option('look_for_keys'), device_params=device_params, allow_agent=self._play_context.allow_agent, timeout=self.get_option('persistent_connect_timeout'), ssh_config=self._ssh_config)
    except SSHUnknownHostError as exc:
        raise AnsibleConnectionFailure(to_native(exc))
    except ImportError as exc:
        raise AnsibleError('connection=netconf is not supported on {0}'.format(self._network_os))
    if (not self._manager.connected):
        return (1, b'', b'not connected')
    self.queue_message('log', 'ncclient manager object created successfully')
    self._connected = True
    super(Connection, self)._connect()
    return (0, to_bytes(self._manager.session_id, errors='surrogate_or_strict'), b'')
