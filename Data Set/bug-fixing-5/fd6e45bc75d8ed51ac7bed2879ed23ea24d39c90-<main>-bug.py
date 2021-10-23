def main():
    ' main entry point for module execution\n    '
    element_spec = dict(name=dict(), configured_password=dict(no_log=True), update_password=dict(default='always', choices=['on_create', 'always']), roles=dict(type='list', aliases=['role']), sshkey=dict(), state=dict(default='present', choices=['present', 'absent']))
    aggregate_spec = deepcopy(element_spec)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec, aliases=['collection', 'users']), purge=dict(type='bool', default=False))
    argument_spec.update(element_spec)
    argument_spec.update(nxos_argument_spec)
    mutually_exclusive = [('name', 'aggregate')]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    warnings = list()
    if (module.params['password'] and (not module.params['configured_password'])):
        warnings.append(('The "password" argument is used to authenticate the current connection. ' + 'To set a user password use "configured_password" instead.'))
    result = {
        'changed': False,
    }
    result['warnings'] = warnings
    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands(update_objects(want, have), module)
    if module.params['purge']:
        want_users = [x['name'] for x in want]
        have_users = [x['name'] for x in have]
        for item in set(have_users).difference(want_users):
            if (item != 'admin'):
                commands.append(('no username %s' % item))
    result['commands'] = commands
    if ('no username admin' in commands):
        module.fail_json(msg='cannot delete the `admin` account')
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    module.exit_json(**result)