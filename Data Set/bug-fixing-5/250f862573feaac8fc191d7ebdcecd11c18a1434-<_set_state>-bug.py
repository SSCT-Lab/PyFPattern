def _set_state(module, state):
    name = module.params['name']
    force = module.params['force']
    want_enabled = (state == 'present')
    state_string = {
        'present': 'enabled',
        'absent': 'disabled',
    }[state]
    a2mod_binary = {
        'present': 'a2enmod',
        'absent': 'a2dismod',
    }[state]
    success_msg = ('Module %s %s' % (name, state_string))
    if (_module_is_enabled(module) != want_enabled):
        if module.check_mode:
            module.exit_json(changed=True, result=success_msg)
        a2mod_binary = module.get_bin_path(a2mod_binary)
        if (a2mod_binary is None):
            module.fail_json(msg=('%s not found. Perhaps this system does not use %s to manage apache' % (a2mod_binary, a2mod_binary)))
        if ((not want_enabled) and force):
            a2mod_binary += ' -f'
        (result, stdout, stderr) = module.run_command(('%s %s' % (a2mod_binary, name)))
        if (_module_is_enabled(module) == want_enabled):
            module.exit_json(changed=True, result=success_msg)
        else:
            module.fail_json(msg=('Failed to set module %s to %s: %s' % (name, state_string, stdout)), rc=result, stdout=stdout, stderr=stderr)
    else:
        module.exit_json(changed=False, result=success_msg)