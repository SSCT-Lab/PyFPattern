def get_nic_inventory(self):
    result = {
        
    }
    nic_list = []
    nic_results = []
    key = 'EthernetInterfaces'
    properties = ['Description', 'FQDN', 'IPv4Addresses', 'IPv6Addresses', 'NameServers', 'PermanentMACAddress', 'SpeedMbps', 'MTUSize', 'AutoNeg', 'Status']
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    if (key not in data):
        return {
            'ret': False,
            'msg': ('Key %s not found' % key),
        }
    ethernetinterfaces_uri = data[key]['@odata.id']
    response = self.get_request((self.root_uri + ethernetinterfaces_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for nic in data['Members']:
        nic_list.append(nic['@odata.id'])
    for n in nic_list:
        nic = {
            
        }
        uri = (self.root_uri + n)
        response = self.get_request(uri)
        if (response['ret'] is False):
            return response
        data = response['data']
        for property in properties:
            if (property in data):
                nic[property] = data[property]
        nic_results.append(nic)
    result['entries'] = nic_results
    return result