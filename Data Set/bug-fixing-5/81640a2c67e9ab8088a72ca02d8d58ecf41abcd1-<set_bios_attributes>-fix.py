def set_bios_attributes(self, attr):
    result = {
        
    }
    key = 'Bios'
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
    bios_uri = data[key]['@odata.id']
    response = self.get_request((self.root_uri + bios_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    set_bios_attr_uri = data['@Redfish.Settings']['SettingsObject']['@odata.id']
    bios_attr = (((('{"' + attr['bios_attr_name']) + '":"') + attr['bios_attr_value']) + '"}')
    payload = {
        'Attributes': json.loads(bios_attr),
    }
    response = self.patch_request((self.root_uri + set_bios_attr_uri), payload, HEADERS)
    if (response['ret'] is False):
        return response
    return {
        'ret': True,
    }