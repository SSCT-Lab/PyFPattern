@property
def compute_client(self):
    self.log('Getting compute client')
    if (not self._compute_client):
        self.check_client_version('compute', compute_client_version, AZURE_EXPECTED_VERSIONS['compute_client_version'])
        self._compute_client = ComputeManagementClient(self.azure_credentials, self.subscription_id, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-03-30')
    return self._compute_client