def _connect(self, check_vm_credentials=True):
    if (not HAS_REQUESTS):
        raise AnsibleError(('%s : %s' % (missing_required_lib('requests'), REQUESTS_IMP_ERR)))
    if (not HAS_PYVMOMI):
        raise AnsibleError(('%s : %s' % (missing_required_lib('PyVmomi'), PYVMOMI_IMP_ERR)))
    super(Connection, self)._connect()
    if (not self.connected):
        self._establish_connection()
        self._establish_vm(check_vm_credentials=check_vm_credentials)
        self._connected = True