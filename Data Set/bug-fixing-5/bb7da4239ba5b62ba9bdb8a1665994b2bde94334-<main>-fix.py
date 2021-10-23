def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(schema=dict(type='str', required=True), template=dict(type='str', required=True), bd=dict(type='str', aliases=['name']), display_name=dict(type='str'), intersite_bum_traffic=dict(type='bool'), optimize_wan_bandwidth=dict(type='bool'), layer2_stretch=dict(type='bool'), layer2_unknown_unicast=dict(type='str', choices=['flood', 'proxy']), layer3_multicast=dict(type='bool'), vrf=dict(type='dict', options=mso_reference_spec()), subnets=dict(type='list', options=mso_subnet_spec()), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['bd']], ['state', 'present', ['bd', 'vrf']]])
    schema = module.params['schema']
    template = module.params['template']
    bd = module.params['bd']
    display_name = module.params['display_name']
    intersite_bum_traffic = module.params['intersite_bum_traffic']
    optimize_wan_bandwidth = module.params['optimize_wan_bandwidth']
    layer2_stretch = module.params['layer2_stretch']
    layer2_unknown_unicast = module.params['layer2_unknown_unicast']
    layer3_multicast = module.params['layer3_multicast']
    vrf = module.params['vrf']
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
    bds = [b['name'] for b in schema_obj['templates'][template_idx]['bds']]
    if ((bd is not None) and (bd in bds)):
        bd_idx = bds.index(bd)
        mso.existing = schema_obj['templates'][template_idx]['bds'][bd_idx]
    if (state == 'query'):
        if (bd is None):
            mso.existing = schema_obj['templates'][template_idx]['bds']
        elif (not mso.existing):
            mso.fail_json(msg="BD '{bd}' not found".format(bd=bd))
        mso.exit_json()
    bds_path = '/templates/{0}/bds'.format(template)
    bd_path = '/templates/{0}/bds/{1}'.format(template, bd)
    ops = []
    mso.previous = mso.existing
    if (state == 'absent'):
        if mso.existing:
            mso.sent = mso.existing = {
                
            }
            ops.append(dict(op='remove', path=bd_path))
    elif (state == 'present'):
        vrf_ref = mso.make_reference(vrf, 'vrf', schema_id, template)
        subnets = mso.make_subnets(subnets)
        if ((display_name is None) and (not mso.existing)):
            display_name = bd
        if ((subnets is None) and (not mso.existing)):
            subnets = []
        payload = dict(name=bd, displayName=display_name, intersiteBumTrafficAllow=intersite_bum_traffic, optimizeWanBandwidth=optimize_wan_bandwidth, l2UnknownUnicast=layer2_unknown_unicast, l2Stretch=layer2_stretch, l3MCast=layer3_multicast, subnets=subnets, vrfRef=vrf_ref)
        mso.sanitize(payload, collate=True)
        if mso.existing:
            ops.append(dict(op='replace', path=bd_path, value=mso.sent))
        else:
            ops.append(dict(op='add', path=(bds_path + '/-'), value=mso.sent))
        mso.existing = mso.proposed
    if (not module.check_mode):
        mso.request(schema_path, method='PATCH', data=ops)
    mso.exit_json()