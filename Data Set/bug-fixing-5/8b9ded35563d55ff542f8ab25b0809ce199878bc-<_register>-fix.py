def _register(self, key):
    try:
        resource_client = self.rm_client
        resource_client.providers.register(key)
    except Exception as exc:
        self.log('One-time registration of {0} failed - {1}'.format(key, str(exc)))
        self.log('You might need to register {0} using an admin account'.format(key))
        self.log('To register a provider using the Python CLI: https://docs.microsoft.com/azure/azure-resource-manager/resource-manager-common-deployment-errors#noregisteredproviderfound')