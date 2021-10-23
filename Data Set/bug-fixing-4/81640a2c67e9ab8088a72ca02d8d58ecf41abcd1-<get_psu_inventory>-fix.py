def get_psu_inventory(self):
    result = {
        
    }
    psu_list = []
    psu_results = []
    key = 'PoweredBy'
    properties = ['Name', 'Model', 'SerialNumber', 'PartNumber', 'Manufacturer', 'FirmwareVersion', 'PowerCapacityWatts', 'PowerSupplyType', 'Status']
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    if ('Links' not in data):
        return {
            'ret': False,
            'msg': 'Property not found',
        }
    if (key not in data['Links']):
        return {
            'ret': False,
            'msg': ('Key %s not found' % key),
        }
    for psu in data['Links']['PoweredBy']:
        psu_list.append(psu['@odata.id'])
    for p in psu_list:
        psu = {
            
        }
        uri = (self.root_uri + p)
        response = self.get_request(uri)
        if (response['ret'] is False):
            return response
        result['ret'] = True
        data = response['data']
        for property in properties:
            if (property in data):
                psu[property] = data[property]
        psu_results.append(psu)
    result['entries'] = psu_results
    return result