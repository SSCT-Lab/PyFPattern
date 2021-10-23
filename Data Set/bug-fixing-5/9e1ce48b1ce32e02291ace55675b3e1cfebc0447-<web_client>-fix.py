@property
def web_client(self):
    self.log('Getting web client')
    if (not self._web_client):
        self._web_client = self.get_mgmt_svc_client(WebSiteManagementClient, base_url=self._cloud_environment.endpoints.resource_manager)
    return self._web_client