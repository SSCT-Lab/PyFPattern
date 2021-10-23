def get_manager_attributes(self):
    result = {
        
    }
    manager_attributes = {
        
    }
    key = 'Attributes'
    response = self.get_request((((self.root_uri + self.manager_uri) + '/') + key))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    if (key not in data):
        return {
            'ret': False,
            'msg': ('Key %s not found' % key),
        }
    for attribute in data[key].items():
        manager_attributes[attribute[0]] = attribute[1]
    result['entries'] = manager_attributes
    return result