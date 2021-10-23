def get_fan_inventory(self):
    result = {
        
    }
    fan_details = []
    key = 'Thermal'
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
                fan_details.append(dict(Name=device['FanName'], RPMs=device['Reading'], State=device['Status']['State'], Health=device['Status']['Health']))
            result['entries'] = fan_details
    return result