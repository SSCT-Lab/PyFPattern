@property
def network_client(self):
    self.log('Getting network client')
    if (not self._network_client):
        self.check_client_version('network', network_client_version, AZURE_EXPECTED_VERSIONS['network_client_version'])
        self._network_client = NetworkManagementClient(self.azure_credentials, self.subscription_id, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-06-01')
    return self._network_client