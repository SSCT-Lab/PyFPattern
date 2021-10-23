@property
def dns_client(self):
    self.log('Getting dns client')
    if (not self._dns_client):
        self.check_client_version('dns', dns_client_version, AZURE_EXPECTED_VERSIONS['dns_client_version'])
        self._dns_client = DnsManagementClient(self.azure_credentials, self.subscription_id, base_url=self._cloud_environment.endpoints.resource_manager)
        self._register('Microsoft.Dns')
    return self._dns_client