def main():
    argument_spec = dict(vrf=dict(required=False, type='str', default='default'), ospf=dict(required=True, type='str'), router_id=dict(required=False, type='str'), default_metric=dict(required=False, type='str'), log_adjacency=dict(required=False, type='str', choices=['log', 'detail', 'default']), timer_throttle_lsa_start=dict(required=False, type='str'), timer_throttle_lsa_hold=dict(required=False, type='str'), timer_throttle_lsa_max=dict(required=False, type='str'), timer_throttle_spf_start=dict(required=False, type='str'), timer_throttle_spf_hold=dict(required=False, type='str'), timer_throttle_spf_max=dict(required=False, type='str'), auto_cost=dict(required=False, type='str'), passive_interface=dict(required=False, type='bool'), state=dict(choices=['present', 'absent'], default='present', required=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = dict(changed=False, commands=[], warnings=warnings)
    state = module.params['state']
    args = PARAM_TO_COMMAND_KEYMAP.keys()
    existing = get_existing(module, args)
    proposed_args = dict(((k, v) for (k, v) in module.params.items() if ((v is not None) and (k in args))))
    proposed = {
        
    }
    for (key, value) in proposed_args.items():
        if (key != 'interface'):
            if (str(value).lower() == 'true'):
                value = True
            elif (str(value).lower() == 'false'):
                value = False
            elif (str(value).lower() == 'default'):
                value = PARAM_TO_DEFAULT_KEYMAP.get(key)
                if (value is None):
                    value = 'default'
            if (existing.get(key) != value):
                proposed[key] = value
    candidate = CustomNetworkConfig(indent=3)
    if (state == 'present'):
        state_present(module, existing, proposed, candidate)
    if ((state == 'absent') and existing):
        state_absent(module, existing, proposed, candidate)
    if candidate:
        candidate = candidate.items_text()
        result['commands'] = candidate
        if (not module.check_mode):
            load_config(module, candidate)
            result['changed'] = True
    module.exit_json(**result)