def main():
    module = AnsibleModule(argument_spec=dict(key=dict(required=True, default=None, type='str'), value_type=dict(required=False, choices=['int', 'bool', 'float', 'string'], type='str'), value=dict(required=False, default=None, type='str'), state=dict(required=True, default=None, choices=['present', 'get', 'absent'], type='str'), direct=dict(required=False, default=False, type='bool'), config_source=dict(required=False, default=None, type='str')), supports_check_mode=True)
    state_values = {
        'present': 'set',
        'absent': 'unset',
        'get': 'get',
    }
    direct = False
    key = module.params['key']
    value_type = module.params['value_type']
    if (module.params['value'].lower() == 'true'):
        value = 'true'
    elif (module.params['value'] == 'false'):
        value = 'false'
    else:
        value = module.params['value']
    state = state_values[module.params['state']]
    if (module.params['direct'] in BOOLEANS_TRUE):
        direct = True
    config_source = module.params['config_source']
    change = False
    new_value = ''
    if (state != 'get'):
        if ((value is None) or (value == '')):
            module.fail_json(msg=('State %s requires "value" to be set' % str(state)))
        elif ((value_type is None) or (value_type == '')):
            module.fail_json(msg=('State %s requires "value_type" to be set' % str(state)))
        if (direct and (config_source is None)):
            module.fail_json(msg=('If "direct" is "yes" then the ' + '"config_source" must be specified'))
        elif ((not direct) and (config_source is not None)):
            module.fail_json(msg=('If the "config_source" is specified ' + 'then "direct" must be "yes"'))
    gconf_pref = GConf2Preference(module, key, value_type, value, direct, config_source)
    (_, current_value) = gconf_pref.call('get')
    if (current_value != value):
        if module.check_mode:
            change = True
            new_value = value
        else:
            (change, new_value) = gconf_pref.call(state)
    else:
        new_value = current_value
    facts = {
        
    }
    facts['gconftool2'] = {
        'changed': change,
        'key': key,
        'value_type': value_type,
        'new_value': new_value,
        'previous_value': current_value,
        'playbook_value': module.params['value'],
    }
    module.exit_json(changed=change, ansible_facts=facts)