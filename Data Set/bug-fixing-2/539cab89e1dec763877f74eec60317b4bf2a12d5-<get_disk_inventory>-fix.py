

def get_disk_inventory(self):
    result = {
        'entries': [],
    }
    controller_list = []
    disk_results = []
    properties = ['BlockSizeBytes', 'CapableSpeedGbs', 'CapacityBytes', 'EncryptionAbility', 'EncryptionStatus', 'FailurePredicted', 'HotspareType', 'Id', 'Identifiers', 'Manufacturer', 'MediaType', 'Model', 'Name', 'PartNumber', 'PhysicalLocation', 'Protocol', 'Revision', 'RotationSpeedRPM', 'SerialNumber', 'Status']
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    data = response['data']
    if (('SimpleStorage' not in data) and ('Storage' not in data)):
        return {
            'ret': False,
            'msg': 'SimpleStorage and Storage resource                      not found',
        }
    if ('Storage' in data):
        storage_uri = data['Storage']['@odata.id']
        response = self.get_request((self.root_uri + storage_uri))
        if (response['ret'] is False):
            return response
        result['ret'] = True
        data = response['data']
        if data['Members']:
            for controller in data['Members']:
                controller_list.append(controller['@odata.id'])
            for c in controller_list:
                uri = (self.root_uri + c)
                response = self.get_request(uri)
                if (response['ret'] is False):
                    return response
                data = response['data']
                if ('Drives' in data):
                    for device in data['Drives']:
                        disk_uri = (self.root_uri + device['@odata.id'])
                        response = self.get_request(disk_uri)
                        data = response['data']
                        disk_result = {
                            
                        }
                        for property in properties:
                            if (property in data):
                                if (data[property] is not None):
                                    disk_result[property] = data[property]
                        disk_results.append(disk_result)
            result['entries'].append(disk_results)
    if ('SimpleStorage' in data):
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
                disk_result = {
                    
                }
                for property in properties:
                    if (property in device):
                        disk_result[property] = device[property]
                disk_results.append(disk_result)
        result['entries'].append(disk_results)
    return result
