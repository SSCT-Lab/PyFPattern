

def _needs_update(module, aggregate):
    new_metadata = (module.params['metadata'] or {
        
    })
    new_metadata['availability_zone'] = module.params['availability_zone']
    if ((module.params['name'] != aggregate.name) or ((module.params['hosts'] is not None) and (module.params['hosts'] != aggregate.hosts)) or ((module.params['availability_zone'] is not None) and (module.params['availability_zone'] != aggregate.availability_zone)) or ((module.params['metadata'] is not None) and (new_metadata != aggregate.metadata))):
        return True
    return False
