def get_manager_attributes(self):
    result = {
        
    }
    manager_attributes = {
        
    }
    attributes_id = 'Attributes'
    response = self.get_request((((self.root_uri + self.manager_uri) + '/') + attributes_id))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for attribute in data['Attributes'].items():
        manager_attributes[attribute[0]] = attribute[1]
    result['entries'] = manager_attributes
    return result