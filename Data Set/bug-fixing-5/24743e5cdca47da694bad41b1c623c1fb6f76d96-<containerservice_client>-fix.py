@property
def containerservice_client(self):
    self.log('Getting container service client')
    if (not self._containerservice_client):
        self._containerservice_client = self.get_mgmt_svc_client(ContainerServiceClient)
    return self._containerservice_client