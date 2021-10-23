@property
def storage_client(self):
    self.log('Getting storage client...')
    if (not self._storage_client):
        self.check_client_version('storage', storage_client_version, AZURE_EXPECTED_VERSIONS['storage_client_version'])
        self._storage_client = StorageManagementClient(self.azure_credentials, self.subscription_id, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-06-01')
    return self._storage_client