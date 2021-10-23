def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(schema=dict(type='str', required=True), template=dict(type='str', required=True), anp=dict(type='str', required=True), epg=dict(type='str', aliases=['name']), bd=dict(type='dict', options=mso_reference_spec()), display_name=dict(type='str'), useg_epg=dict(type='bool'), intra_epg_isolation=dict(type='str', choices=['enforced', 'unenforced']), intersite_multicaste_source=dict(type='bool'), subnets=dict(type='list', options=mso_subnet_spec()), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['epg']], ['state', 'present', ['epg']]])
    schema = module.params['schema']
    template = module.params['template']
    anp = module.params['anp']
    epg = module.params['epg']
    display_name = module.params['display_name']
    bd = module.params['bd']
    useg_epg = module.params['useg_epg']
    intra_epg_isolation = module.params['intra_epg_isolation']
    intersite_multicaste_source = module.params['intersite_multicaste_source']
    subnets = module.params['subnets']
    state = module.params['state']
    mso = MSOModule(module)
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
    anps = [a['name'] for a in schema_obj['templates'][template_idx]['anps']]
    if (anp not in anps):
        mso.fail_json(msg="Provided anp '{0}' does not exist. Existing anps: {1}".format(anp, ', '.join(anps)))
    anp_idx = anps.index(anp)
    epgs = [e['name'] for e in schema_obj['templates'][template_idx]['anps'][anp_idx]['epgs']]
    if ((epg is not None) and (epg in epgs)):
        epg_idx = epgs.index(epg)
        mso.existing = schema_obj['templates'][template_idx]['anps'][anp_idx]['epgs'][epg_idx]
    if (state == 'query'):
        if (epg is None):
            mso.existing = schema_obj['templates'][template_idx]['anps'][anp_idx]['epgs']
        elif (not mso.existing):
            mso.fail_json(msg="EPG '{epg}' not found".format(epg=epg))
        mso.exit_json()
    epgs_path = '/templates/{0}/anps/{1}/epgs'.format(template, anp)
    epg_path = '/templates/{0}/anps/{1}/epgs/{2}'.format(template, anp, epg)
    ops = []
    mso.previous = mso.existing
    if (state == 'absent'):
        if mso.existing:
            mso.sent = mso.existing = {
                
            }
            ops.append(dict(op='remove', path=epg_path))
    elif (state == 'present'):
        bd_ref = mso.make_reference(bd, 'bd', schema_id, template)
        subnets = mso.make_subnets(subnets)
        if ((display_name is None) and (not mso.existing)):
            display_name = epg
        payload = dict(name=epg, displayName=display_name, uSegEpg=useg_epg, intraEpg=intra_epg_isolation, proxyArp=intersite_multicaste_source, contractRelationships=[], subnets=subnets, bdRef=bd_ref)
        mso.sanitize(payload, collate=True)
        if mso.existing:
            ops.append(dict(op='replace', path=epg_path, value=mso.sent))
        else:
            ops.append(dict(op='add', path=(epgs_path + '/-'), value=mso.sent))
        mso.existing = mso.proposed
    if (not module.check_mode):
        mso.request(schema_path, method='PATCH', data=ops)
    mso.exit_json()