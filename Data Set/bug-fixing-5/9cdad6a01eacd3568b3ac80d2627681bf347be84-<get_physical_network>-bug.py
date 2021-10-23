def get_physical_network(self, key=None):
    physical_network = self.module.params.get('physical_network')
    if self.physical_network:
        return self._get_by_key(key, self.physical_network)
    args = {
        'zoneid': self.get_zone(key='id'),
    }
    physical_networks = self.query_api('listPhysicalNetworks', **args)
    if physical_networks:
        for net in physical_networks['physicalnetwork']:
            if (physical_network.lower() in [net['name'].lower(), net['id']]):
                self.physical_network = net
                self.result['physical_network'] = net['name']
                break
    return self._get_by_key(key, self.physical_network)