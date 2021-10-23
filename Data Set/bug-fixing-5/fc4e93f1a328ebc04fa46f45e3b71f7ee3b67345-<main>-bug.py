def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(schema=dict(type='str', required=True), template=dict(type='str', required=True), anp=dict(type='str', required=False, aliases=['name']), display_name=dict(type='str'), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['anp']], ['state', 'present', ['anp']]])
    schema = module.params['schema']
    template = module.params['template']
    anp = module.params['anp']
    display_name = module.params['display_name']
    state = module.params['state']
    mso = MSOModule(module)
    schema_obj = mso.get_obj('schemas', displayName=schema)
    if schema_obj:
        schema_id = schema_obj['id']
    else:
        mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))
    path = 'schemas/{id}'.format(id=schema_id)
    templates = [t['name'] for t in schema_obj['templates']]
    if (template not in templates):
        mso.fail_json(msg="Provided template '{0}' does not exist. Existing templates: {1}".format(template, ', '.join(templates)))
    template_idx = templates.index(template)
    anps = [a['name'] for a in schema_obj['templates'][template_idx]['anps']]
    if ((anp is not None) and (anp in anps)):
        anp_idx = anps.index(anp)
        mso.existing = schema_obj['templates'][template_idx]['anps'][anp_idx]
    if (state == 'query'):
        if (anp is None):
            mso.existing = schema_obj['templates'][template_idx]['anps']
        elif (not mso.existing):
            mso.fail_json(msg="ANP '{anp}' not found".format(anp=anp))
        mso.exit_json()
    mso.previous = mso.existing
    if (state == 'absent'):
        if mso.existing:
            mso.sent = mso.existing = {
                
            }
            operation = [dict(op='remove', path='/templates/{template}/anps/{anp}'.format(template=template, anp=anp))]
            if (not module.check_mode):
                mso.request(path, method='PATCH', data=operation)
    elif (state == 'present'):
        if ((display_name is None) and (not mso.existing)):
            display_name = anp
        payload = dict(name=anp, displayName=display_name, epgs=[])
        mso.sanitize(payload, collate=True)
        if mso.existing:
            operation = [dict(op='replace', path='/templates/{template}/anps/{anp}'.format(template=template, anp=anp), value=mso.sent)]
        else:
            operation = [dict(op='add', path='/templates/{template}/anps/-'.format(template=template), value=mso.sent)]
        mso.existing = mso.proposed
        if (not module.check_mode):
            mso.request(path, method='PATCH', data=operation)
    mso.exit_json()