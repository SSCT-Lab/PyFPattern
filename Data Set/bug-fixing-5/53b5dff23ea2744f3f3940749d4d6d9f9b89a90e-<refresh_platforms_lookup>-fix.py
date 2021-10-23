def refresh_platforms_lookup(self):
    url = (self.api_endpoint + '/api/dcim/platforms/?limit=0')
    platforms = self.get_resource_list(api_url=url)
    self.platforms_lookup = dict(((platform['id'], platform['name']) for platform in platforms))