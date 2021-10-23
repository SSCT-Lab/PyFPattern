def create_static_nat(self, ip_address):
    self.result['changed'] = True
    args = {
        
    }
    args['virtualmachineid'] = self.get_vm(key='id')
    args['ipaddressid'] = ip_address['id']
    args['vmguestip'] = self.get_vm_guest_ip()
    args['networkid'] = self.get_network(key='id')
    if (not self.module.check_mode):
        res = self.cs.enableStaticNat(**args)
        if ('errortext' in res):
            self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
        self.ip_address = None
        ip_address = self.get_ip_address()
    return ip_address