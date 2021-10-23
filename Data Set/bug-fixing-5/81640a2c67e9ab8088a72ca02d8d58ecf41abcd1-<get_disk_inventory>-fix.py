def get_disk_inventory(self):
    result = {
        
    }
    controller_list = []
    disk_results = []
    properties = ['Name', 'Manufacturer', 'Model', 'Status', 'CapacityBytes']
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    data = response['data']
    if ('SimpleStorage' not in data):
        return {
            'ret': False,
            'msg': 'SimpleStorage resource not found',
        }
    storage_uri = data['SimpleStorage']['@odata.id']
    response = self.get_request((self.root_uri + storage_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for controller in data['Members']:
        controller_list.append(controller['@odata.id'])
    for c in controller_list:
        uri = (self.root_uri + c)
        response = self.get_request(uri)
        if (response['ret'] is False):
            return response
        data = response['data']
        for device in data['Devices']:
            disk = {
                
            }
            for property in properties:
                if (property in device):
                    disk[property] = device[property]
            disk_results.append(disk)
    result['entries'] = disk_results
    return result