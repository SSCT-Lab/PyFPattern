def _connect(self):
    super(Connection, self)._connect()
    display.display('ssh connection done, stating ncclient', log_only=True)
    allow_agent = True
    if (self._play_context.password is not None):
        allow_agent = False
    key_filename = None
    if self._play_context.private_key_file:
        key_filename = os.path.expanduser(self._play_context.private_key_file)
    if (not self._network_os):
        raise AnsibleConnectionError('network_os must be set for netconf connections')
    try:
        self._manager = manager.connect(host=self._play_context.remote_addr, port=(self._play_context.port or 830), username=self._play_context.remote_user, password=self._play_context.password, key_filename=str(key_filename), hostkey_verify=C.HOST_KEY_CHECKING, look_for_keys=C.PARAMIKO_LOOK_FOR_KEYS, allow_agent=allow_agent, timeout=self._play_context.timeout, device_params={
            'name': self._network_os,
        })
    except SSHUnknownHostError as exc:
        raise AnsibleConnectionFailure(str(exc))
    if (not self._manager.connected):
        return (1, '', 'not connected')
    display.display('ncclient manager object created successfully', log_only=True)
    self._connected = True
    return (0, self._manager.session_id, '')