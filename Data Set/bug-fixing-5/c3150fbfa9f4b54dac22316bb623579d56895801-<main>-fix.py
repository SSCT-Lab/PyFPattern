def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(src=dict(), force=dict(default=False, type='bool'), include_defaults=dict(default=True, type='bool'), backup=dict(default=False, type='bool'), config=dict())
    argument_spec.update(nxos_argument_spec)
    mutually_exclusive = [('config', 'backup'), ('config', 'force')]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    result = dict(changed=False)
    candidate = NetworkConfig(contents=module.params['src'], indent=2)
    contents = get_current_config(module)
    if contents:
        config = NetworkConfig(contents=contents, indent=2)
        result['__backup__'] = str(contents)
    if (not module.params['force']):
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
    result['commands'] = commands
    module.exit_json(**result)