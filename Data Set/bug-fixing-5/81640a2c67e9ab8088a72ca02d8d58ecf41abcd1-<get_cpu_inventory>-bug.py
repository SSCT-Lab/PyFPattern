def get_cpu_inventory(self):
    result = {
        
    }
    cpu_details = []
    cpu_list = []
    key = 'Processors'
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    processors_uri = data[key]['@odata.id']
    response = self.get_request((self.root_uri + processors_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for cpu in data['Members']:
        cpu_list.append(cpu['@odata.id'])
    for c in cpu_list:
        uri = (self.root_uri + c)
        response = self.get_request(uri)
        if (response['ret'] is False):
            return response
        data = response['data']
        cpu_details.append(dict(Name=data['Id'], Manufacturer=data['Manufacturer'], Model=data['Model'], MaxSpeedMHz=data['MaxSpeedMHz'], TotalCores=data['TotalCores'], TotalThreads=data['TotalThreads'], State=data['Status']['State'], Health=data['Status']['Health']))
    result['entries'] = cpu_details
    return result