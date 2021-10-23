def get_fan_inventory(self):
    result = {
        
    }
    fan_results = []
    key = 'Thermal'
    properties = ['FanName', 'Reading', 'ReadingUnits', 'Status']
    for chassis_uri in self.chassis_uri_list:
        response = self.get_request((self.root_uri + chassis_uri))
        if (response['ret'] is False):
            return response
        result['ret'] = True
        data = response['data']
        if (key in data):
            thermal_uri = data[key]['@odata.id']
            response = self.get_request((self.root_uri + thermal_uri))
            if (response['ret'] is False):
                return response
            result['ret'] = True
            data = response['data']
            for device in data['Fans']:
                fan = {
                    
                }
                for property in properties:
                    if (property in device):
                        fan[property] = device[property]
                fan_results.append(fan)
    result['entries'] = fan_results
    return result