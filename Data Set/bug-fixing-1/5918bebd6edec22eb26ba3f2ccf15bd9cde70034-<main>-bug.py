

def main():
    argument_spec = dict(src=dict(type='str', default=None), filter=dict(type='str', default=''))
    argument_spec.update(fortios_argument_spec)
    required_if = fortios_required_if
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)
    result = dict(changed=False)
    if (not HAS_PYFG):
        module.fail_json(msg='Could not import the python library pyFG required by this module')
    f = FortiOS(module.params['host'], username=module.params['username'], password=module.params['password'], timeout=module.params['username'], vdom=module.params['vdom'])
    try:
        f.open()
    except:
        module.fail_json(msg='Error connecting device')
    try:
        f.load_config(path=module.params['filter'])
        result['running_config'] = f.running_config.to_text()
    except:
        module.fail_json(msg='Error reading running config')
    if module.params['backup']:
        backup(module, f.running_config.to_text())
    if (module.params['src'] is not None):
        try:
            conf_str = open(module.params['src'], 'r').read()
            f.load_config(in_candidate=True, config_text=conf_str)
        except:
            module.fail_json(msg="Can't open configuration file, or configuration invalid")
        change_string = f.compare_config()
        c = FortiConfig()
        c.parse_config_output(change_string)
        for o in NOT_UPDATABLE_CONFIG_OBJECTS:
            c.del_block(o)
        change_string = c.to_text()
        if (change_string != ''):
            result['change_string'] = change_string
            result['changed'] = True
        if ((module.check_mode is False) and (change_string != '')):
            try:
                f.commit(change_string)
            except CommandExecutionException:
                e = get_exception()
                module.fail_json(msg='Unable to execute command, check your args, the error was {0}'.format(e.message))
            except FailedCommit:
                e = get_exception()
                module.fail_json(msg='Unable to commit, check your args, the error was {0}'.format(e.message))
            except ForcedCommit:
                e = get_exception()
                module.fail_json(msg='Failed to force commit, check your args, the error was {0}'.format(e.message))
    module.exit_json(**result)
