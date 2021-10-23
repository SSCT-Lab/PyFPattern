def refresh_manufacturers_lookup(self):
    url = urljoin(self.api_endpoint, '/api/dcim/manufacturers/?limit=0')
    manufacturers = self.get_resource_list(api_url=url)
    self.manufacturers_lookup = dict(((manufacturer['id'], manufacturer['name']) for manufacturer in manufacturers))