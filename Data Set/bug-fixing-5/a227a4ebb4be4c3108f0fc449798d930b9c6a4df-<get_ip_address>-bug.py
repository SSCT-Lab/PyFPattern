def get_ip_address(self, key=None):
    if self.ip_address:
        return self._get_by_key(key, self.ip_address)
    ip_address = self.module.params.get('ip_address')
    args = {
        'ipaddress': self.module.params.get('ip_address'),
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'projectid': self.get_project(key='id'),
        'vpcid': self.get_vpc(key='id'),
    }
    ip_addresses = self.cs.listPublicIpAddresses(**args)
    if ip_addresses:
        self.ip_address = ip_addresses['publicipaddress'][0]
    return self._get_by_key(key, self.ip_address)