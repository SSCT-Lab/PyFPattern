def refresh_racks_lookup(self):
    url = urljoin(self.api_endpoint, '/api/dcim/racks/?limit=0')
    racks = self.get_resource_list(api_url=url)
    self.racks_lookup = dict(((rack['id'], rack['name']) for rack in racks))