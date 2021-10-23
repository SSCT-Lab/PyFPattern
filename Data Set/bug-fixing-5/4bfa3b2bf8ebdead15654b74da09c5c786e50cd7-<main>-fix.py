def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(contract=dict(type='str', aliases=['contract_name']), subject=dict(type='str', aliases=['contract_subject', 'name', 'subject_name']), tenant=dict(type='str', aliases=['tenant_name']), priority=dict(type='str', choices=['unspecified', 'level1', 'level2', 'level3']), reverse_filter=dict(type='bool'), dscp=dict(type='str', aliases=['target'], choices=['AF11', 'AF12', 'AF13', 'AF21', 'AF22', 'AF23', 'AF31', 'AF32', 'AF33', 'AF41', 'AF42', 'AF43', 'CS0', 'CS1', 'CS2', 'CS3', 'CS4', 'CS5', 'CS6', 'CS7', 'EF', 'VA', 'unspecified']), description=dict(type='str', aliases=['descr']), consumer_match=dict(type='str', choices=['all', 'at_least_one', 'at_most_one', 'none']), provider_match=dict(type='str', choices=['all', 'at_least_one', 'at_most_one', 'none']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['contract', 'subject', 'tenant']], ['state', 'present', ['contract', 'subject', 'tenant']]])
    aci = ACIModule(module)
    subject = module.params['subject']
    priority = module.params['priority']
    reverse_filter = aci.boolean(module.params['reverse_filter'])
    contract = module.params['contract']
    dscp = module.params['dscp']
    description = module.params['description']
    consumer_match = module.params['consumer_match']
    if (consumer_match is not None):
        consumer_match = MATCH_MAPPING[consumer_match]
    provider_match = module.params['provider_match']
    if (provider_match is not None):
        provider_match = MATCH_MAPPING[provider_match]
    state = module.params['state']
    tenant = module.params['tenant']
    aci.construct_url(root_class=dict(aci_class='fvTenant', aci_rn='tn-{0}'.format(tenant), module_object=tenant, target_filter={
        'name': tenant,
    }), subclass_1=dict(aci_class='vzBrCP', aci_rn='brc-{0}'.format(contract), module_object=contract, target_filter={
        'name': contract,
    }), subclass_2=dict(aci_class='vzSubj', aci_rn='subj-{0}'.format(subject), module_object=subject, target_filter={
        'name': subject,
    }))
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='vzSubj', class_config=dict(name=subject, prio=priority, revFltPorts=reverse_filter, targetDscp=dscp, consMatchT=consumer_match, provMatchT=provider_match, descr=description))
        aci.get_diff(aci_class='vzSubj')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()