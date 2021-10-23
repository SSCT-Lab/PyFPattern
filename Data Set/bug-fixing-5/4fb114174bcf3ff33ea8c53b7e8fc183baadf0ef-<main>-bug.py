def main():
    argument_spec = dict(flush_routes=dict(type='bool'), enforce_rtr_alert=dict(type='bool'), restart=dict(type='bool', default=False), state=dict(choices=['present', 'default'], default='present'), include_defaults=dict(default=False), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    state = module.params['state']
    restart = module.params['restart']
    if ((state == 'default') and ((module.params['flush_routes'] is not None) or (module.params['enforce_rtr_alert'] is not None))):
        module.fail_json(msg='When state=default other params have no effect.')
    args = ['flush_routes', 'enforce_rtr_alert']
    existing = invoke('get_existing', module, args)
    end_state = existing
    proposed = dict(((k, v) for (k, v) in module.params.items() if ((v is not None) and (k in args))))
    proposed_args = proposed.copy()
    if (state == 'default'):
        proposed_args = dict(((k, False) for k in args))
    result = {
        
    }
    if ((state == 'present') or ((state == 'default') and (True in existing.values())) or restart):
        candidate = CustomNetworkConfig(indent=3)
        invoke('get_commands', module, existing, proposed_args, candidate)
        response = load_config(module, candidate)
        result.update(response)
    else:
        result['updates'] = []
    if restart:
        proposed['restart'] = restart
    result['connected'] = module.connected
    if (module._verbosity > 0):
        end_state = invoke('get_existing', module, args)
        result['end_state'] = end_state
        result['existing'] = existing
        result['proposed'] = proposed
    result['warnings'] = warnings
    module.exit_json(**result)