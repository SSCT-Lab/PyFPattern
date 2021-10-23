def get_system_inventory(self):
    result = {
        
    }
    inventory = {
        
    }
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    inventory['Status'] = data['Status']['Health']
    inventory['HostName'] = data['HostName']
    inventory['PowerState'] = data['PowerState']
    inventory['Model'] = data['Model']
    inventory['Manufacturer'] = data['Manufacturer']
    inventory['PartNumber'] = data['PartNumber']
    inventory['SystemType'] = data['SystemType']
    inventory['AssetTag'] = data['AssetTag']
    inventory['ServiceTag'] = data['SKU']
    inventory['SerialNumber'] = data['SerialNumber']
    inventory['BiosVersion'] = data['BiosVersion']
    inventory['MemoryTotal'] = data['MemorySummary']['TotalSystemMemoryGiB']
    inventory['MemoryHealth'] = data['MemorySummary']['Status']['Health']
    inventory['CpuCount'] = data['ProcessorSummary']['Count']
    inventory['CpuModel'] = data['ProcessorSummary']['Model']
    inventory['CpuHealth'] = data['ProcessorSummary']['Status']['Health']
    datadict = data['Boot']
    if ('BootSourceOverrideMode' in datadict.keys()):
        inventory['BootSourceOverrideMode'] = data['Boot']['BootSourceOverrideMode']
    else:
        inventory['BootSourceOverrideMode'] = 'Not available'
    if ('TrustedModules' in data):
        for d in data['TrustedModules']:
            if ('InterfaceType' in d.keys()):
                inventory['TPMInterfaceType'] = d['InterfaceType']
            inventory['TPMStatus'] = d['Status']['State']
    else:
        inventory['TPMInterfaceType'] = 'Not available'
        inventory['TPMStatus'] = 'Not available'
    result['entries'] = inventory
    return result