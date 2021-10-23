def main():
    ' Entry point for ansible module. '
    argument_spec = {
        'state': {
            'default': 'present',
            'choices': ['present', 'absent'],
        },
        'table': {
            'required': True,
        },
        'record': {
            'required': True,
        },
        'col': {
            'required': True,
        },
        'key': {
            'required': True,
        },
        'value': {
            'required': True,
        },
        'timeout': {
            'default': 5,
            'type': 'int',
        },
    }
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    result = {
        'changed': False,
    }
    module.params['ovs-vsctl'] = module.get_bin_path('ovs-vsctl', True)
    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    command = map_obj_to_command(want, have, module)
    result['command'] = command
    if command:
        if (not module.check_mode):
            module.run_command(command, check_rc=True)
        result['changed'] = True
    module.exit_json(**result)