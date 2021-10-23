def build_entity(self):
    provider_type = self._provider_type(requires_authentication=(self._module.params.get('username') is not None))
    if (self._module.params.pop('type') == 'network'):
        setattr(provider_type, 'type', otypes.OpenStackNetworkProviderType(self._module.params.pop('network_type')))
    for (key, value) in self._module.params.items():
        if hasattr(provider_type, key):
            setattr(provider_type, key, value)
    return provider_type