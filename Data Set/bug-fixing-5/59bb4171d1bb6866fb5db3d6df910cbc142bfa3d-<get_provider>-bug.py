def get_provider(self):
    from sentry.plugins import bindings
    if self.provider.startswith('integrations:'):
        provider_cls = bindings.get('integration-repository.provider').get(self.provider)
        return provider_cls(self.provider)
    provider_cls = bindings.get('repository.provider').get(self.provider)
    return provider_cls(self.provider)