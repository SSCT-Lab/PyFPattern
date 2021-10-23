def get_firmware_inventory(self):
    result = {
        
    }
    firmware = {
        
    }
    response = self.get_request((self.root_uri + self.firmware_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for device in data['Members']:
        d = device['@odata.id']
        d = d.replace(self.firmware_uri, '')
        if ('Installed' in d):
            uri = ((self.root_uri + self.firmware_uri) + d)
            response = self.get_request(uri)
            if (response['ret'] is False):
                return response
            result['ret'] = True
            data = response['data']
            firmware[data['Name']] = data['Version']
    result['entries'] = firmware
    return result