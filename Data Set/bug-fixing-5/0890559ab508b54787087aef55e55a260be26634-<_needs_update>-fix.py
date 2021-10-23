def _needs_update(module, domain):
    if ((module.params['description'] is not None) and (domain.description != module.params['description'])):
        return True
    if (domain.enabled != module.params['enabled']):
        return True
    return False