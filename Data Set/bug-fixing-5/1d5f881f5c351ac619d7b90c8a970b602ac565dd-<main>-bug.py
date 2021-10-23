def main():
    spec = dict(gather_subset=dict(default=['!config'], type='list'))
    spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    capabilities = get_capabilities(module)
    if capabilities:
        os_version = capabilities['device_info']['network_os_version']
        os_version_major = int(os_version[0])
        if ((os_version_major < 7) and ('6.0(2)A8' not in os_version)):
            module.fail_json(msg='this module requires JSON structured output support on the NX-OS device')
    warnings = list()
    check_args(module, warnings)
    gather_subset = module.params['gather_subset']
    runable_subsets = set()
    exclude_subsets = set()
    for subset in gather_subset:
        if (subset == 'all'):
            runable_subsets.update(VALID_SUBSETS)
            continue
        if subset.startswith('!'):
            subset = subset[1:]
            if (subset == 'all'):
                exclude_subsets.update(VALID_SUBSETS)
                continue
            exclude = True
        else:
            exclude = False
        if (subset not in VALID_SUBSETS):
            module.fail_json(msg='Bad subset')
        if exclude:
            exclude_subsets.add(subset)
        else:
            runable_subsets.add(subset)
    if (not runable_subsets):
        runable_subsets.update(VALID_SUBSETS)
    runable_subsets.difference_update(exclude_subsets)
    runable_subsets.add('default')
    facts = dict()
    facts['gather_subset'] = list(runable_subsets)
    instances = list()
    for key in runable_subsets:
        instances.append(FACT_SUBSETS[key](module))
    for inst in instances:
        inst.populate()
        facts.update(inst.facts)
        warnings.extend(inst.warnings)
    ansible_facts = dict()
    for (key, value) in iteritems(facts):
        if key.startswith('_'):
            ansible_facts[key[1:]] = value
        else:
            key = ('ansible_net_%s' % key)
            ansible_facts[key] = value
    module.exit_json(ansible_facts=ansible_facts, warnings=warnings)