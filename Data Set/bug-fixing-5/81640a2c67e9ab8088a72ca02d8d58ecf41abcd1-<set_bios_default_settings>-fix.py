def set_bios_default_settings(self):
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
    reset_bios_settings_uri = data['Actions']['#Bios.ResetBios']['target']
    response = self.post_request((self.root_uri + reset_bios_settings_uri), {
        
    }, HEADERS)
    if (response['ret'] is False):
        return response
    return {
        'ret': True,
    }