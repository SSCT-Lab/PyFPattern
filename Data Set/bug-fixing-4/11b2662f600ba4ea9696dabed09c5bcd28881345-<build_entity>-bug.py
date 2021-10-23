def build_entity(self):
    provider_type = self._provider_type(requires_authentication=('username' in self._module.params))
    for (key, value) in self._module.params.items():
        if hasattr(provider_type, key):
            setattr(provider_type, key, value)
    return provider_type