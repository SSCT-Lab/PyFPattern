def main():
    argument_spec = dict(user=dict(required=True, type='str'), group=dict(type='str', required=True), pwd=dict(type='str'), privacy=dict(type='str'), authentication=dict(choices=['md5', 'sha']), encrypt=dict(type='bool'), state=dict(choices=['absent', 'present'], default='present'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, required_together=[['authentication', 'pwd'], ['encrypt', 'privacy']], supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    results = {
        'changed': False,
        'commands': [],
        'warnings': warnings,
    }
    user = module.params['user']
    group = module.params['group']
    pwd = module.params['pwd']
    privacy = module.params['privacy']
    encrypt = module.params['encrypt']
    authentication = module.params['authentication']
    state = module.params['state']
    if (privacy and encrypt):
        if ((not pwd) and authentication):
            module.fail_json(msg='pwd and authentication must be provided when using privacy and encrypt')
    if (group and (group not in get_snmp_groups(module))):
        module.fail_json(msg='group not configured yet on switch.')
    existing = get_snmp_user(user, module)
    if existing:
        if (group not in existing['group']):
            existing['group'] = None
        else:
            existing['group'] = group
    commands = []
    if ((state == 'absent') and existing):
        commands.append(remove_snmp_user(user))
    elif (state == 'present'):
        new = False
        reset = False
        args = dict(user=user, pwd=pwd, group=group, privacy=privacy, encrypt=encrypt, authentication=authentication)
        proposed = dict(((k, v) for (k, v) in args.items() if (v is not None)))
        if (not existing):
            if encrypt:
                proposed['encrypt'] = 'aes-128'
            commands.append(config_snmp_user(proposed, user, reset, new))
        elif existing:
            if (encrypt and (not existing['encrypt'].startswith('aes'))):
                reset = True
                proposed['encrypt'] = 'aes-128'
            delta = dict(set(proposed.items()).difference(existing.items()))
            if delta.get('pwd'):
                delta['authentication'] = authentication
            if delta:
                delta['group'] = group
            if (delta and encrypt):
                delta['encrypt'] = 'aes-128'
            command = config_snmp_user(delta, user, reset, new)
            commands.append(command)
    cmds = flatten_list(commands)
    if cmds:
        results['changed'] = True
        if (not module.check_mode):
            load_config(module, cmds)
        if ('configure' in cmds):
            cmds.pop(0)
        results['commands'] = cmds
    module.exit_json(**results)