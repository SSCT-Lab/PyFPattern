def add_nic(self):
    self.result['changed'] = True
    args = {
        'virtualmachineid': self.get_vm(key='id'),
        'networkid': self.get_network(key='id'),
        'ipaddress': self.module.params.get('ip_address'),
    }
    if (not self.module.check_mode):
        res = self.query_api('addNicToVirtualMachine', **args)
        if ('errortext' in res):
            self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
        if self.module.params.get('poll_async'):
            vm = self.poll_job(res, 'virtualmachine')
            self.nic = self.get_nic_from_result(result=vm)
    return self.nic