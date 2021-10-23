def refresh_tenants_lookup(self):
    url = urljoin(self.api_endpoint, '/api/tenancy/tenants/?limit=0')
    tenants = self.get_resource_list(api_url=url)
    self.tenants_lookup = dict(((tenant['id'], tenant['name']) for tenant in tenants))