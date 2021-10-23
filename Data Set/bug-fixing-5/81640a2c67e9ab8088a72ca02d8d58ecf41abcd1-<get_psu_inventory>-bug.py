def get_psu_inventory(self):
    result = {
        
    }
    psu_details = []
    psu_list = []
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for psu in data['Links']['PoweredBy']:
        psu_list.append(psu['@odata.id'])
    for p in psu_list:
        uri = (self.root_uri + p)
        response = self.get_request(uri)
        if (response['ret'] is False):
            return response
        result['ret'] = True
        data = response['data']
        psu = {
            
        }
        psu['Name'] = data['Name']
        psu['Model'] = data['Model']
        psu['SerialNumber'] = data['SerialNumber']
        psu['PartNumber'] = data['PartNumber']
        if ('Manufacturer' in data):
            psu['Manufacturer'] = data['Manufacturer']
        psu['FirmwareVersion'] = data['FirmwareVersion']
        psu['PowerCapacityWatts'] = data['PowerCapacityWatts']
        psu['PowerSupplyType'] = data['PowerSupplyType']
        psu['Status'] = data['Status']['State']
        psu['Health'] = data['Status']['Health']
        psu_details.append(psu)
    result['entries'] = psu_details
    return result