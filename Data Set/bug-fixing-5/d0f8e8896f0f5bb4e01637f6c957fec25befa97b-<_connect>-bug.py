def _connect(self):
    if (not HAS_REQUESTS):
        raise AnsibleError(('%s : %s' % (missing_required_lib('requests'), REQUESTS_IMP_ERR)))
    if (not HAS_PYVMOMI):
        raise AnsibleError(('%s : %s' % (missing_required_lib('PyVmomi'), PYVMOMI_IMP_ERR)))
    super(Connection, self)._connect()
    if self.connected:
        pass
    self._establish_connection()
    self._establish_vm()
    self._connected = True