def _connect(self):
    if (not HAS_WINRM):
        raise AnsibleError(('winrm or requests is not installed: %s' % to_text(WINRM_IMPORT_ERR)))
    elif (not HAS_XMLTODICT):
        raise AnsibleError(('xmltodict is not installed: %s' % to_text(XMLTODICT_IMPORT_ERR)))
    super(Connection, self)._connect()
    if (not self.protocol):
        self.protocol = self._winrm_connect()
        self._connected = True
    return self