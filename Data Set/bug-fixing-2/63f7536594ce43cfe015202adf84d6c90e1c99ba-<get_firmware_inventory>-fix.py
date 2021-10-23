

def get_firmware_inventory(self):
    result = {
        
    }
    response = self.get_request((self.root_uri + self.firmware_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    result['entries'] = []
    for device in data['Members']:
        uri = (self.root_uri + device['@odata.id'])
        response = self.get_request(uri)
        if (response['ret'] is False):
            return response
        result['ret'] = True
        data = response['data']
        firmware = {
            
        }
        for key in ['Name', 'Id', 'Status', 'Version', 'Updateable', 'SoftwareId', 'LowestSupportedVersion', 'Manufacturer', 'ReleaseDate']:
            if (key in data):
                firmware[key] = data.get(key)
        result['entries'].append(firmware)
    return result
