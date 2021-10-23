@property
def network_client(self):
    self.log('Getting network client')
    if (not self._network_client):
        self._network_client = self.get_mgmt_svc_client(NetworkManagementClient, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-06-01')
    return self._network_client