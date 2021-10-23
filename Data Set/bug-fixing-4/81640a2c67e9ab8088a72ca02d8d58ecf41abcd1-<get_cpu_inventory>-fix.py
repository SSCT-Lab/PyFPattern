def get_cpu_inventory(self):
    result = {
        
    }
    cpu_list = []
    cpu_results = []
    key = 'Processors'
    properties = ['Id', 'Manufacturer', 'Model', 'MaxSpeedMHz', 'TotalCores', 'TotalThreads', 'Status']
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
    processors_uri = data[key]['@odata.id']
    response = self.get_request((self.root_uri + processors_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for cpu in data['Members']:
        cpu_list.append(cpu['@odata.id'])
    for c in cpu_list:
        cpu = {
            
        }
        uri = (self.root_uri + c)
        response = self.get_request(uri)
        if (response['ret'] is False):
            return response
        data = response['data']
        for property in properties:
            if (property in data):
                cpu[property] = data[property]
        cpu_results.append(cpu)
    result['entries'] = cpu_results
    return result