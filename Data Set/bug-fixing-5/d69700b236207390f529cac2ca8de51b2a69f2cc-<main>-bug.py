def main():
    argument_spec = dict(vni=dict(required=True, type='str'), route_distinguisher=dict(required=False, type='str'), route_target_both=dict(required=False, type='list'), route_target_import=dict(required=False, type='list'), route_target_export=dict(required=False, type='list'), state=dict(choices=['present', 'absent'], default='present', required=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    results = dict(changed=False, warnings=warnings)
    state = module.params['state']
    args = PARAM_TO_COMMAND_KEYMAP.keys()
    existing = get_existing(module, args)
    proposed_args = dict(((k, v) for (k, v) in module.params.items() if ((v is not None) and (k in args))))
    commands = []
    parents = []
    proposed = {
        
    }
    for (key, value) in proposed_args.items():
        if (key != 'vni'):
            if (value == 'true'):
                value = True
            elif (value == 'false'):
                value = False
            if (existing.get(key) != value):
                proposed[key] = value
    if (state == 'present'):
        (commands, parents) = state_present(module, existing, proposed)
    elif ((state == 'absent') and existing):
        (commands, parents) = state_absent(module, existing, proposed)
    if commands:
        candidate = CustomNetworkConfig(indent=3)
        candidate.add(commands, parents=parents)
        candidate = candidate.items_text()
        load_config(module, candidate)
        results['changed'] = True
        results['commands'] = candidate
    else:
        results['commands'] = []
    module.exit_json(**results)