

def main():
    argument_spec = aci_argument_spec()
    argument_spec.update({
        'leaf_interface_profile': dict(type='str', aliases=['leaf_interface_profile_name']),
        'access_port_selector': dict(type='str', aliases=['name', 'access_port_selector_name']),
        'description': dict(typ='str'),
        'leaf_port_blk': dict(type='str', aliases=['leaf_port_blk_name']),
        'leaf_port_blk_description': dict(type='str'),
        'from': dict(type='str', aliases=['fromPort', 'from_port_range']),
        'to': dict(type='str', aliases=['toPort', 'to_port_range']),
        'policy_group': dict(type='str', aliases=['policy_group_name']),
        'interface_type': dict(type='str', default='switch_port', choices=['fex', 'port_channel', 'switch_port', 'vpc']),
        'state': dict(type='str', default='present', choices=['absent', 'present', 'query']),
    })
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['leaf_interface_profile', 'access_port_selector']], ['state', 'present', ['leaf_interface_profile', 'access_port_selector']]])
    leaf_interface_profile = module.params['leaf_interface_profile']
    access_port_selector = module.params['access_port_selector']
    description = module.params['description']
    leaf_port_blk = module.params['leaf_port_blk']
    leaf_port_blk_description = module.params['leaf_port_blk_description']
    from_ = module.params['from']
    to_ = module.params['to']
    policy_group = module.params['policy_group']
    interface_type = module.params['interface_type']
    state = module.params['state']
    aci = ACIModule(module)
    aci.construct_url(root_class=dict(aci_class='infraAccPortP', aci_rn='infra/accportprof-{0}'.format(leaf_interface_profile), filter_target='eq(infraAccPortP.name, "{0}")'.format(leaf_interface_profile), module_object=leaf_interface_profile), subclass_1=dict(aci_class='infraHPortS', aci_rn='hports-{0}-typ-range'.format(access_port_selector), filter_target='eq(infraHPortS.name, "{0}")'.format(access_port_selector), module_object=access_port_selector), child_classes=['infraPortBlk', 'infraRsAccBaseGrp'])
    INTERFACE_TYPE_MAPPING = dict(fex='uni/infra/funcprof/accportgrp-{0}'.format(policy_group), port_channel='uni/infra/funcprof/accbundle-{0}'.format(policy_group), switch_port='uni/infra/funcprof/accportgrp-{0}'.format(policy_group), vpc='uni/infra/funcprof/accbundle-{0}'.format(policy_group))
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='infraHPortS', class_config=dict(descr=description, name=access_port_selector), child_configs=[dict(infraPortBlk=dict(attributes=dict(descr=leaf_port_blk_description, name=leaf_port_blk, fromPort=from_, toPort=to_))), dict(infraRsAccBaseGrp=dict(attributes=dict(tDn=INTERFACE_TYPE_MAPPING[interface_type])))])
        aci.get_diff(aci_class='infraHPortS')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()
