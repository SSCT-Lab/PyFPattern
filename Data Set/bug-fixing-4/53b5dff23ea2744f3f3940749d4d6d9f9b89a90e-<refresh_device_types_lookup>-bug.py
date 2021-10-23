def refresh_device_types_lookup(self):
    url = urljoin(self.api_endpoint, '/api/dcim/device-types/?limit=0')
    device_types = self.get_resource_list(api_url=url)
    self.device_types_lookup = dict(((device_type['id'], device_type['model']) for device_type in device_types))