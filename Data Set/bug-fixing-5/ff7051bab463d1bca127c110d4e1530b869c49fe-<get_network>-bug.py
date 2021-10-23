def get_network(self, key=None):
    'Return a network dictionary or the value of given key of.'
    if self.network:
        return self._get_by_key(key, self.network)
    network = self.module.params.get('network')
    if (not network):
        return None
    args = {
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'projectid': self.get_project(key='id'),
        'zoneid': self.get_zone(key='id'),
        'vpcid': self.get_vpc(key='id'),
    }
    networks = self.cs.listNetworks(**args)
    if (not networks):
        self.module.fail_json(msg='No networks available.')
    for n in networks['network']:
        if (network in [n['displaytext'], n['name'], n['id']]):
            self.network = n
            return self._get_by_key(key, self.network)
    self.module.fail_json(msg=("Network '%s' not found" % network))