def associate_ip_address(self, ip_address):
    self.result['changed'] = True
    args = {
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'projectid': self.get_project(key='id'),
        'networkid': self.get_network(key='id'),
        'zoneid': self.get_zone(key='id'),
        'vpcid': self.get_vpc(key='id'),
    }
    ip_address = None
    if (not self.module.check_mode):
        res = self.cs.associateIpAddress(**args)
        poll_async = self.module.params.get('poll_async')
        if poll_async:
            ip_address = self.poll_job(res, 'ipaddress')
    return ip_address