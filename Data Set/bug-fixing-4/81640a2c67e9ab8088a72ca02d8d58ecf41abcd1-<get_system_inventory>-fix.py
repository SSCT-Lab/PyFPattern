def get_system_inventory(self):
    result = {
        
    }
    inventory = {
        
    }
    properties = ['Status', 'HostName', 'PowerState', 'Model', 'Manufacturer', 'PartNumber', 'SystemType', 'AssetTag', 'ServiceTag', 'SerialNumber', 'BiosVersion', 'MemorySummary', 'ProcessorSummary', 'TrustedModules']
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for property in properties:
        if (property in data):
            inventory[property] = data[property]
    result['entries'] = inventory
    return result