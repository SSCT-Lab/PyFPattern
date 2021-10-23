def get_network(self):
    if (not self.network):
        network = self.module.params.get('name')
        args = {
            
        }
        args['zoneid'] = self.get_zone(key='id')
        args['projectid'] = self.get_project(key='id')
        args['account'] = self.get_account(key='name')
        args['domainid'] = self.get_domain(key='id')
        networks = self.cs.listNetworks(**args)
        if networks:
            for n in networks['network']:
                if (network in [n['name'], n['displaytext'], n['id']]):
                    self.network = n
                    break
    return self.network