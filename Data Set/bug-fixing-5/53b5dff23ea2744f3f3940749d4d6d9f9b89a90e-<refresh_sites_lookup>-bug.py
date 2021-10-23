def refresh_sites_lookup(self):
    url = urljoin(self.api_endpoint, '/api/dcim/sites/?limit=0')
    sites = self.get_resource_list(api_url=url)
    self.sites_lookup = dict(((site['id'], site['name']) for site in sites))