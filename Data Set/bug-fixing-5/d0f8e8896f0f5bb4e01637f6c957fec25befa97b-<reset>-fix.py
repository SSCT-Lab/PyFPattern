def reset(self):
    'Reset the connection to vcenter.'
    self.close()
    self._connect(check_vm_credentials=False)