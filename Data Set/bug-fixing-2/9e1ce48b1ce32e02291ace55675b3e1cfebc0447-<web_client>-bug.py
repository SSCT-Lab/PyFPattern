

@property
def web_client(self):
    self.log('Getting web client')
    if (not self._web_client):
        self._web_client = self.get_mgmt_svc_client(WebSiteManagementClient, base_url=self.base_url)
    return self._web_client
