

def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(schema=dict(type='str', required=True), template=dict(type='str', required=True), anp=dict(type='str', required=True), epg=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    argument_spec.update(mso_subnet_spec())
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['subnet']], ['state', 'present', ['subnet']]])
    schema = module.params['schema']
    template = module.params['template']
    anp = module.params['anp']
    epg = module.params['epg']
    subnet = module.params['subnet']
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
        mso.fail_json(msg="Provided template '{template}' does not exist. Existing templates: {templates}".format(template=template, templates=', '.join(templates)))
    template_idx = templates.index(template)
    anps = [a['name'] for a in schema_obj['templates'][template_idx]['anps']]
    if (anp not in anps):
        mso.fail_json(msg="Provided anp '{anp}' does not exist. Existing anps: {anps}".format(anp=anp, anps=', '.join(anps)))
    anp_idx = anps.index(anp)
    epgs = [e['name'] for e in schema_obj['templates'][template_idx]['anps'][anp_idx]['epgs']]
    if (epg not in epgs):
        mso.fail_json(msg="Provided epg '{epg}' does not exist. Existing epgs: {epgs}".format(epg=epg, epgs=', '.join(epgs)))
    epg_idx = epgs.index(epg)
    subnets = [s['ip'] for s in schema_obj['templates'][template_idx]['anps'][anp_idx]['epgs'][epg_idx]['subnets']]
    if (subnet in subnets):
        subnet_idx = subnets.index(subnet)
        subnet_path = '/templates/{0}/anps/{1}/epgs/{2}/subnets/{3}'.format(template, anp, epg, subnet_idx)
        mso.existing = schema_obj['templates'][template_idx]['anps'][anp_idx]['epgs'][epg_idx]['subnets'][subnet_idx]
    if (state == 'query'):
        if (subnet is None):
            mso.existing = schema_obj['templates'][template_idx]['anps'][anp_idx]['epgs'][epg_idx]['subnets']
        elif (not mso.existing):
            mso.fail_json(msg="Subnet '{subnet}' not found".format(subnet=subnet))
        mso.exit_json()
    subnets_path = '/templates/{0}/anps/{1}/epgs/{2}/subnets'.format(template, anp, epg)
    ops = []
    mso.previous = mso.existing
    if (state == 'absent'):
        if mso.existing:
            mso.existing = {
                
            }
            ops.append(dict(op='remove', path=subnet_path))
    elif (state == 'present'):
        if (not mso.existing):
            if (description is None):
                description = subnet
            if (scope is None):
                scope = 'private'
            if (shared is None):
                shared = False
            if (no_default_gateway is None):
                no_default_gateway = False
        payload = dict(ip=subnet, description=description, scope=scope, shared=shared, noDefaultGateway=no_default_gateway)
        mso.sanitize(payload, collate=True)
        if mso.existing:
            ops.append(dict(op='replace', path=subnet_path, value=mso.sent))
        else:
            ops.append(dict(op='add', path=(subnets_path + '/-'), value=mso.sent))
        mso.existing = mso.proposed
    if (not module.check_mode):
        mso.request(schema_path, method='PATCH', data=ops)
    mso.exit_json()
