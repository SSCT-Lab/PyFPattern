def get_network_offering(self, key=None):
    network_offering = self.module.params.get('network_offering')
    if (not network_offering):
        self.module.fail_json(msg='missing required arguments: network_offering')
    args = {
        
    }
    args['zoneid'] = self.get_zone(key='id')
    network_offerings = self.cs.listNetworkOfferings(**args)
    if network_offerings:
        for no in network_offerings['networkoffering']:
            if (network_offering in [no['name'], no['displaytext'], no['id']]):
                return self._get_by_key(key, no)
    self.module.fail_json(msg=("Network offering '%s' not found" % network_offering))