def main():
    module = AnsibleModule(argument_spec=dict(domain=dict(default='NSGlobalDomain', required=False), host=dict(default=None, required=False), key=dict(default=None), type=dict(default='string', required=False, choices=['array', 'bool', 'boolean', 'date', 'float', 'int', 'integer', 'string']), array_add=dict(default=False, required=False, type='bool'), value=dict(default=None, required=False), state=dict(default='present', required=False, choices=['absent', 'present']), path=dict(default='/usr/bin:/usr/local/bin', required=False)), supports_check_mode=True)
    domain = module.params['domain']
    host = module.params['host']
    key = module.params['key']
    type = module.params['type']
    array_add = module.params['array_add']
    value = module.params['value']
    state = module.params['state']
    path = module.params['path']
    try:
        defaults = OSXDefaults(module=module, domain=domain, host=host, key=key, type=type, array_add=array_add, value=value, state=state, path=path)
        changed = defaults.run()
        module.exit_json(changed=changed)
    except OSXDefaultsException:
        e = get_exception()
        module.fail_json(msg=e.message)