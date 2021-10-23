@property
def rm_client(self):
    self.log('Getting resource manager client')
    if (not self._resource_client):
        self._resource_client = self.get_mgmt_svc_client(ResourceManagementClient, base_url=self._cloud_environment.endpoints.resource_manager, api_version='2017-05-10')
    return self._resource_client