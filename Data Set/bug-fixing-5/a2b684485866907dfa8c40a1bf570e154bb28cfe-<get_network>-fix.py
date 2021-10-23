def get_network(self):
    if (not self.network):
        network = self.module.params.get('name')
        args = {
            'zoneid': self.get_zone(key='id'),
            'projectid': self.get_project(key='id'),
            'account': self.get_account(key='name'),
            'domainid': self.get_domain(key='id'),
        }
        networks = self.cs.listNetworks(**args)
        if networks:
            for n in networks['network']:
                if (network in [n['name'], n['displaytext'], n['id']]):
                    self.network = n
                    break
    return self.network