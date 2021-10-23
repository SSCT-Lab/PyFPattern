def get_nic(self):
    if self.nic:
        return self.nic
    args = {
        'virtualmachineid': self.get_vm(key='id'),
        'networkid': self.get_network(key='id'),
    }
    nics = self.cs.listNics(**args)
    if nics:
        self.nic = nics['nic'][0]
        return self.nic
    self.module.fail_json(msg=('NIC for VM %s in network %s not found' % (self.get_vm(key='name'), self.get_network(key='name'))))