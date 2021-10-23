def refresh_device_roles_lookup(self):
    url = urljoin(self.api_endpoint, '/api/dcim/device-roles/?limit=0')
    device_roles = self.get_resource_list(api_url=url)
    self.device_roles_lookup = dict(((device_role['id'], device_role['name']) for device_role in device_roles))