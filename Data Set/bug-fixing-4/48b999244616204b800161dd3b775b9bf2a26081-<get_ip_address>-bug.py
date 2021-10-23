def get_ip_address(self, key=None):
    if self.ip_address:
        return self._get_by_key(key, self.ip_address)
    args = {
        'ipaddress': self.module.params.get('ip_address'),
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'projectid': self.get_project(key='id'),
        'vpcid': self.get_vpc(key='id'),
    }
    ip_addresses = self.cs.listPublicIpAddresses(**args)
    if ip_addresses:
        tags = self.module.params.get('tags')
        for ip_addr in ip_addresses['publicipaddress']:
            if (ip_addr['ipaddress'] == args['ipaddress'] != ''):
                self.ip_address = ip_addresses['publicipaddress'][0]
            elif tags:
                if (sorted([tag for tag in tags if (tag in ip_addr['tags'])]) == sorted(tags)):
                    self.ip_address = ip_addr
    return self._get_by_key(key, self.ip_address)