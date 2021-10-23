@property
def web_client(self):
    self.log('Getting web client')
    if (not self._web_client):
        self.check_client_version('web', web_client_version, AZURE_EXPECTED_VERSIONS['web_client_version'])
        self._web_client = WebSiteManagementClient(credentials=self.azure_credentials, subscription_id=self.subscription_id, base_url=self.base_url)
        self._register('Microsoft.Web')
    return self._web_client