def get_nic_inventory(self):
    result = {
        
    }
    nic_details = []
    nic_list = []
    key = 'EthernetInterfaces'
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
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
        nic['Name'] = data['Name']
        nic['FQDN'] = data['FQDN']
        for d in data['IPv4Addresses']:
            nic['IPv4'] = d['Address']
            if ('GateWay' in d):
                nic['Gateway'] = d['GateWay']
            nic['SubnetMask'] = d['SubnetMask']
        for d in data['IPv6Addresses']:
            nic['IPv6'] = d['Address']
        for d in data['NameServers']:
            nic['NameServers'] = d
        nic['MACAddress'] = data['PermanentMACAddress']
        nic['SpeedMbps'] = data['SpeedMbps']
        nic['MTU'] = data['MTUSize']
        nic['AutoNeg'] = data['AutoNeg']
        if ('Status' in data):
            nic['Health'] = data['Status']['Health']
            nic['State'] = data['Status']['State']
        nic_details.append(nic)
    result['entries'] = nic_details
    return result