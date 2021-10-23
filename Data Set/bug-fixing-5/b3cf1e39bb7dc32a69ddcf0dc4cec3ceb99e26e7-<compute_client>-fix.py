@property
def compute_client(self):
    self.log('Getting compute client')
    if (not self._compute_client):
        self._compute_client = self.get_mgmt_svc_client(ComputeManagementClient, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-03-30')
    return self._compute_client