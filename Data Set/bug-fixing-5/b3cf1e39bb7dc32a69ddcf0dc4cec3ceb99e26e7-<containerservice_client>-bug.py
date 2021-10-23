@property
def containerservice_client(self):
    self.log('Getting container service client')
    if (not self._containerservice_client):
        self._containerservice_client = ContainerServiceClient(self.azure_credentials, self.subscription_id)
    return self._containerservice_client