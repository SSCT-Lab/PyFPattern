def get_storage_controller_inventory(self):
    result = {
        
    }
    controller_list = []
    controller_results = []
    properties = ['CacheSummary', 'FirmwareVersion', 'Identifiers', 'Location', 'Manufacturer', 'Model', 'Name', 'PartNumber', 'SerialNumber', 'SpeedGbps', 'Status']
    key = 'StorageControllers'
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    data = response['data']
    if ('Storage' not in data):
        return {
            'ret': False,
            'msg': 'Storage resource not found',
        }
    storage_uri = data['Storage']['@odata.id']
    response = self.get_request((self.root_uri + storage_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    if data['Members']:
        for storage_member in data['Members']:
            storage_member_uri = storage_member['@odata.id']
            response = self.get_request((self.root_uri + storage_member_uri))
            data = response['data']
            if (key in data):
                controller_list = data[key]
                for controller in controller_list:
                    controller_result = {
                        
                    }
                    for property in properties:
                        if (property in controller):
                            controller_result[property] = controller[property]
                    controller_results.append(controller_result)
            result['entries'] = controller_results
        return result
    else:
        return {
            'ret': False,
            'msg': 'Storage resource not found',
        }