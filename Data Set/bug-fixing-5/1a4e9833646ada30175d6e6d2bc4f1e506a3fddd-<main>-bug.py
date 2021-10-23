def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(schema=dict(type='str', required=True), template=dict(type='str', required=True), contract=dict(type='str', required=True), contract_display_name=dict(type='str'), contract_scope=dict(type='str', choices=['application-profile', 'global', 'tenant', 'vrf']), contract_filter_type=dict(type='str', choices=['both-way', 'one-way']), filter=dict(type='str', aliases=['name']), filter_template=dict(type='str'), filter_schema=dict(type='str'), filter_type=dict(type='str', default='both-way', choices=FILTER_KEYS.keys(), aliases=['type']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['filter']], ['state', 'present', ['filter']]])
    schema = module.params['schema']
    template = module.params['template']
    contract = module.params['contract']
    contract_display_name = module.params['contract_display_name']
    contract_filter_type = module.params['contract_filter_type']
    contract_scope = module.params['contract_scope']
    filter_name = module.params['filter']
    filter_template = module.params['filter_template']
    filter_schema = module.params['filter_schema']
    filter_type = module.params['filter_type']
    state = module.params['state']
    contract_ftype = ('bothWay' if (contract_filter_type == 'both-way') else 'oneWay')
    if ((contract_filter_type == 'both-way') and (filter_type != 'both-way')):
        module.warn("You are adding 'one-way' filters to a 'both-way' contract")
    elif ((contract_filter_type != 'both-way') and (filter_type == 'both-way')):
        module.warn("You are adding 'both-way' filters to a 'one-way' contract")
    if (filter_template is None):
        filter_template = template
    if (filter_schema is None):
        filter_schema = schema
    filter_key = FILTER_KEYS[filter_type]
    mso = MSOModule(module)
    filter_schema_id = mso.lookup_schema(filter_schema)
    schema_obj = mso.get_obj('schemas', displayName=schema)
    if schema_obj:
        schema_id = schema_obj['id']
    else:
        mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))
    schema_path = 'schemas/{id}'.format(**schema_obj)
    templates = [t['name'] for t in schema_obj['templates']]
    if (template not in templates):
        mso.fail_json(msg="Provided template '{0}' does not exist. Existing templates: {1}".format(template, ', '.join(templates)))
    template_idx = templates.index(template)
    mso.existing = {
        
    }
    contract_idx = None
    filter_idx = None
    contracts = [c['name'] for c in schema_obj['templates'][template_idx]['contracts']]
    if (contract in contracts):
        contract_idx = contracts.index(contract)
        filters = [f['filterRef'] for f in schema_obj['templates'][template_idx]['contracts'][contract_idx][filter_key]]
        filter_ref = mso.filter_ref(schema_id=filter_schema_id, template=filter_template, filter=filter_name)
        if (filter_ref in filters):
            filter_idx = filters.index(filter_ref)
            filter_path = '/templates/{0}/contracts/{1}/{2}/{3}'.format(template, contract, filter_key, filter_idx)
            mso.existing = schema_obj['templates'][template_idx]['contracts'][contract_idx][filter_key][filter_idx]
    if (state == 'query'):
        if (contract_idx is None):
            mso.fail_json(msg="Provided contract '{0}' does not exist. Existing contracts: {1}".format(contract, ', '.join(contracts)))
        if (filter_name is None):
            mso.existing = schema_obj['templates'][template_idx]['contracts'][contract_idx][filter_key]
        elif (not mso.existing):
            mso.fail_json(msg="FilterRef '{filter_ref}' not found".format(filter_ref=filter_ref))
        mso.exit_json()
    ops = []
    contract_path = '/templates/{0}/contracts/{1}'.format(template, contract)
    filters_path = '/templates/{0}/contracts/{1}/{2}'.format(template, contract, filter_key)
    mso.previous = mso.existing
    if (state == 'absent'):
        mso.proposed = mso.sent = {
            
        }
        if (contract_idx is None):
            pass
        elif (filter_idx is None):
            pass
        elif (len(filters) == 1):
            mso.existing = {
                
            }
            ops.append(dict(op='remove', path=contract_path))
        else:
            mso.existing = {
                
            }
            ops.append(dict(op='remove', path=filter_path))
    elif (state == 'present'):
        payload = dict(filterRef=dict(filterName=filter_name, templateName=filter_template, schemaId=filter_schema_id), directives=[])
        mso.sanitize(payload, collate=True)
        mso.existing = mso.sent
        if (contract_idx is None):
            if (not mso.existing):
                if (contract_display_name is None):
                    contract_display_name = contract
                if (contract_filter_type is None):
                    contract_ftype = 'bothWay'
                if (contract_scope is None):
                    contract_scope = 'context'
            payload = {
                'name': contract,
                'displayName': contract_display_name,
                'filterType': contract_ftype,
                'scope': contract_scope,
            }
            ops.append(dict(op='add', path='/templates/{0}/contracts/-'.format(template), value=payload))
        else:
            if (contract_display_name is not None):
                ops.append(dict(op='replace', path=(contract_path + '/displayName'), value=contract_display_name))
            if (contract_filter_type is not None):
                ops.append(dict(op='replace', path=(contract_path + '/filterType'), value=contract_ftype))
            if (contract_scope is not None):
                ops.append(dict(op='replace', path=(contract_path + '/scope'), value=contract_scope))
        if (filter_idx is None):
            ops.append(dict(op='add', path=(filters_path + '/-'), value=mso.sent))
        else:
            ops.append(dict(op='replace', path=filter_path, value=mso.sent))
    if (not module.check_mode):
        mso.request(schema_path, method='PATCH', data=ops)
    mso.exit_json()