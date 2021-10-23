def lock(module, state):
    consul_api = get_consul_api(module)
    session = module.params.get('session')
    key = module.params.get('key')
    value = module.params.get('value')
    if (not session):
        module.fail(msg=('%s of lock for %s requested but no session supplied' % (state, key)))
    (index, existing) = consul_api.kv.get(key)
    changed = ((not existing) or (existing and (existing['Value'] != value)))
    if (changed and (not module.check_mode)):
        if (state == 'acquire'):
            changed = consul_api.kv.put(key, value, cas=module.params.get('cas'), acquire=session, flags=module.params.get('flags'))
        else:
            changed = consul_api.kv.put(key, value, cas=module.params.get('cas'), release=session, flags=module.params.get('flags'))
    module.exit_json(changed=changed, index=index, key=key)