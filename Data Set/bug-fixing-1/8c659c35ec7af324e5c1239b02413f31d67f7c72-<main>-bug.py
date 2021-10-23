

def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(schema=dict(type='str', required=True), template=dict(type='str', required=True), bd=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    argument_spec.update(mso_subnet_spec())
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['ip']], ['state', 'present', ['ip']]])
    schema = module.params['schema']
    template = module.params['template']
    bd = module.params['bd']
    ip = module.params['ip']
    description = module.params['description']
    scope = module.params['scope']
    shared = module.params['shared']
    no_default_gateway = module.params['no_default_gateway']
    state = module.params['state']
    mso = MSOModule(module)
    schema_obj = mso.get_obj('schemas', displayName=schema)
    if (not schema_obj):
        mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))
    schema_path = 'schemas/{id}'.format(**schema_obj)
    templates = [t['name'] for t in schema_obj['templates']]
    if (template not in templates):
        mso.fail_json(msg="Provided template '{0}' does not exist. Existing templates: {1}".format(template, ', '.join(templates)))
    template_idx = templates.index(template)
    bds = [b['name'] for b in schema_obj['templates'][template_idx]['bds']]
    if (bd not in bds):
        mso.fail_json(msg="Provided BD '{0}' does not exist. Existing BDs: {1}".format(bd, ', '.join(bds)))
    bd_idx = bds.index(bd)
    subnets = [s['ip'] for s in schema_obj['templates'][template_idx]['bds'][bd_idx]['subnets']]
    if (ip in subnets):
        ip_idx = subnets.index(ip)
        subnet_path = '/templates/{0}/bds/{1}/subnets/{2}'.format(template, bd, ip_idx)
        mso.existing = schema_obj['templates'][template_idx]['bds'][bd_idx]['subnets'][ip_idx]
    if (state == 'query'):
        if (ip is None):
            mso.existing = schema_obj['templates'][template_idx]['bds'][bd_idx]['subnets']
        elif (not mso.existing):
            mso.fail_json(msg="Subnet '{ip}' not found".format(ip=ip))
        mso.exit_json()
    subnets_path = '/templates/{0}/bds/{1}/subnets'.format(template, bd)
    ops = []
    mso.previous = mso.existing
    if (state == 'absent'):
        if mso.existing:
            mso.sent = mso.existing = {
                
            }
            ops.append(dict(op='remove', path=subnet_path))
    elif (state == 'present'):
        if ((description is None) and (not mso.existing)):
            description = ip
        if ((scope is None) and (not mso.existing)):
            scope = 'private'
        if ((shared is None) and (not mso.existing)):
            shared = False
        if ((no_default_gateway is None) and (not mso.existing)):
            no_default_gateway = False
        payload = dict(ip=ip, description=description, scope=scope, shared=shared, noDefaultGateway=no_default_gateway)
        mso.sanitize(payload, collate=True)
        if mso.existing:
            ops.append(dict(op='replace', path=subnet_path, value=mso.sent))
        else:
            ops.append(dict(op='add', path=(subnets_path + '/-'), value=mso.sent))
        mso.existing = mso.proposed
    if (not module.check_mode):
        mso.request(schema_path, method='PATCH', data=ops)
    mso.exit_json()
