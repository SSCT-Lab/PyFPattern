

def main():
    element_spec = dict(prefix=dict(type='str', aliases=['address']), next_hop=dict(type='str'), vrf=dict(type='str', default='default'), tag=dict(type='str'), route_name=dict(type='str'), pref=dict(type='str', aliases=['admin_distance']), state=dict(choices=['absent', 'present'], default='present'))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['prefix'] = dict(required=True)
    aggregate_spec['next_hop'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec))
    argument_spec.update(element_spec)
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    result = {
        'changed': False,
        'commands': [],
    }
    if warnings:
        result['warnings'] = warnings
    want = map_params_to_obj(module)
    for w in want:
        prefix = normalize_prefix(module, w['prefix'])
        candidate = CustomNetworkConfig(indent=3)
        reconcile_candidate(module, candidate, prefix, w)
        if candidate:
            candidate = candidate.items_text()
            load_config(module, candidate)
            result['commands'].extend(candidate)
            result['changed'] = True
        else:
            result['commands'] = []
    module.exit_json(**result)
