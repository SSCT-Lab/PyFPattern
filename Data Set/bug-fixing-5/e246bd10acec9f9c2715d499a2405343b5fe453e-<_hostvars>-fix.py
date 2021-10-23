def _hostvars(self, host):
    'Return dictionary of all device attributes\n\n        Depending on number of devices in NSoT, could be rather slow since this\n        has to request every device resource to filter through\n        '
    device = [i for i in self.client.devices.get() if (host in i['hostname'])][0]
    attributes = device['attributes']
    attributes.update({
        'site_id': device['site_id'],
        'id': device['id'],
    })
    return attributes