def refresh_regions_lookup(self):
    url = (self.api_endpoint + '/api/dcim/regions/?limit=0')
    regions = self.get_resource_list(api_url=url)
    self.regions_lookup = dict(((region['id'], region['name']) for region in regions))