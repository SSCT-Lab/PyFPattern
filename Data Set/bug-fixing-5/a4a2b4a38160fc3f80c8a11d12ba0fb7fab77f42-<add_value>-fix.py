def add_value(module):
    consul_api = get_consul_api(module)
    key = module.params.get('key')
    value = module.params.get('value')
    (index, changed) = _has_value_changed(consul_api, key, value)
    if (changed and (not module.check_mode)):
        changed = consul_api.kv.put(key, value, cas=module.params.get('cas'), flags=module.params.get('flags'))
    stored = None
    if module.params.get('retrieve'):
        (index, stored) = consul_api.kv.get(key)
    module.exit_json(changed=changed, index=index, key=key, data=stored)