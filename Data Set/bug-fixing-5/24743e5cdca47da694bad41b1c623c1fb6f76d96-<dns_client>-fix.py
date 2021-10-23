@property
def dns_client(self):
    self.log('Getting dns client')
    if (not self._dns_client):
        self._dns_client = self.get_mgmt_svc_client(DnsManagementClient, base_url=self._cloud_environment.endpoints.resource_manager)
    return self._dns_client