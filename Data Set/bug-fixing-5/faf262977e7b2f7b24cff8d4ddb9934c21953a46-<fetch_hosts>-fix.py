def fetch_hosts(self):
    return chain(self.get_resource_list(self.device_url), self.get_resource_list(self.virtual_machines_url))