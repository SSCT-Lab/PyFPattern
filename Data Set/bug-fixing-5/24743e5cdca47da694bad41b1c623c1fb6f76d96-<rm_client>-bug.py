@property
def rm_client(self):
    self.log('Getting resource manager client')
    if (not self._resource_client):
        self.check_client_version('resource', resource_client_version, AZURE_EXPECTED_VERSIONS['resource_client_version'])
        self._resource_client = ResourceManagementClient(self.azure_credentials, self.subscription_id, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-05-10')
    return self._resource_client