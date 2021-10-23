@property
def storage_client(self):
    self.log('Getting storage client...')
    if (not self._storage_client):
        self._storage_client = self.get_mgmt_svc_client(StorageManagementClient, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-06-01')
    return self._storage_client