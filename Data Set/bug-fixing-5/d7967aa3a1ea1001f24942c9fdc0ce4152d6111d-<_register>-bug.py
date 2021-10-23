def _register(self, key):
    try:
        resource_client = self.rm_client
        resource_client.providers.register(key)
    except Exception as exc:
        self.fail('One-time registration of {0} failed - {1}'.format(key, str(exc)))