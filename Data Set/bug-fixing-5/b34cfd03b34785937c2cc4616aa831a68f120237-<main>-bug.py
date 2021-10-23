def main():
    argument_spec = dict(lines=dict(aliases=['commands'], required=True, type='list'), before=dict(type='list'), after=dict(type='list'), match=dict(default='line', choices=['line', 'strict', 'exact']), replace=dict(default='line', choices=['line', 'block']), force=dict(default=False, type='bool'), config=dict())
    argument_spec.update(asa_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    lines = module.params['lines']
    result = {
        'changed': False,
    }
    candidate = NetworkConfig(indent=1)
    candidate.add(lines)
    acl_name = parse_acl_name(module)
    if (not module.params['force']):
        contents = get_acl_config(module, acl_name)
        config = NetworkConfig(indent=1, contents=contents)
        commands = candidate.difference(config)
        commands = dumps(commands, 'commands').split('\n')
        commands = [str(c) for c in commands if c]
    else:
        commands = str(candidate).split('\n')
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    result['updates'] = commands
    module.exit_json(**result)