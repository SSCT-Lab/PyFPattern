def get_disk_inventory(self):
    result = {
        
    }
    disks_details = []
    controller_list = []
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
            disks_details.append(dict(Controller=data['Name'], Name=device['Name'], Manufacturer=device['Manufacturer'], Model=device['Model'], State=device['Status']['State'], Health=device['Status']['Health']))
    result['entries'] = disks_details
    return result