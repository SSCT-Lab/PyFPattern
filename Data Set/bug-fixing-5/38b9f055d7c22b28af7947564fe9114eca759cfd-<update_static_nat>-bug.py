def update_static_nat(self, ip_address):
    args = {
        
    }
    args['virtualmachineid'] = self.get_vm(key='id')
    args['ipaddressid'] = ip_address['id']
    args['vmguestip'] = self.get_vm_guest_ip()
    ip_address['vmguestip'] = ip_address['vmipaddress']
    if self.has_changed(args, ip_address, ['vmguestip', 'virtualmachineid']):
        self.result['changed'] = True
        if (not self.module.check_mode):
            res = self.cs.disableStaticNat(ipaddressid=ip_address['id'])
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            self.poll_job(res, 'staticnat')
            res = self.cs.enableStaticNat(**args)
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            self.ip_address = None
            ip_address = self.get_ip_address()
    return ip_address