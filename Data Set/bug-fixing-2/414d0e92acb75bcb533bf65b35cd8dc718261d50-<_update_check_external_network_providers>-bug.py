

def _update_check_external_network_providers(self, entity):
    if (entity.external_network_providers is None):
        return (not self.param('external_network_providers'))
    entity_providers = self._connection.follow_link(entity.external_network_providers)
    entity_provider_ids = [provider.id for provider in entity_providers]
    entity_provider_names = [provider.name for provider in entity_providers]
    for provider in self._get_external_network_providers():
        if provider.get('id'):
            if (provider.get('id') not in entity_provider_ids):
                return False
        elif (provider.get('name') and (provider.get('name') not in entity_provider_names)):
            return False
    for entity_provider in entity_providers:
        if (not any([self._matches_entity(provider, entity_provider) for provider in self._get_external_network_providers()])):
            return False
    return True
