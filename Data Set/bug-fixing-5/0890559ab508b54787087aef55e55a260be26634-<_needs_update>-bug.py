def _needs_update(module, domain):
    if (domain.description != module.params['description']):
        return True
    if (domain.enabled != module.params['enabled']):
        return True
    return False