def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(tenant=dict(type='str', aliases=['tenant_name']), ap=dict(type='str', aliases=['app_profile', 'app_profile_name']), epg=dict(type='str', aliases=['epg_name']), description=dict(type='str', aliases=['descr']), encap_id=dict(type='int', aliases=['vlan', 'vlan_id']), primary_encap_id=dict(type='int', aliases=['primary_vlan', 'primary_vlan_id']), deploy_immediacy=dict(type='str', choices=['immediate', 'lazy']), interface_mode=dict(type='str', choices=['802.1p', 'access', 'native', 'regular', 'tagged', 'trunk', 'untagged'], aliases=['interface_mode_name', 'mode']), interface_type=dict(type='str', default='switch_port', choices=['fex', 'port_channel', 'switch_port', 'vpc']), pod_id=dict(type='int', aliases=['pod', 'pod_number']), leafs=dict(type='list', aliases=['leaves', 'nodes', 'paths', 'switches']), interface=dict(type='str'), extpaths=dict(type='int'), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['interface_type', 'fex', ['extpaths']], ['state', 'absent', ['ap', 'epg', 'interface', 'leafs', 'pod_id', 'tenant']], ['state', 'present', ['ap', 'encap_id', 'epg', 'interface', 'leafs', 'pod_id', 'tenant']]])
    tenant = module.params['tenant']
    ap = module.params['ap']
    epg = module.params['epg']
    description = module.params['description']
    encap_id = module.params['encap_id']
    primary_encap_id = module.params['primary_encap_id']
    deploy_immediacy = module.params['deploy_immediacy']
    interface_mode = module.params['interface_mode']
    interface_type = module.params['interface_type']
    pod_id = module.params['pod_id']
    leafs = module.params['leafs']
    if (leafs is not None):
        leafs = [str(leaf) for leaf in module.params['leafs']]
        if (len(leafs) == 1):
            if (interface_type != 'vpc'):
                leafs = leafs[0]
            else:
                module.fail_json(msg='A interface_type of "vpc" requires 2 leafs')
        elif (len(leafs) == 2):
            if (interface_type == 'vpc'):
                leafs = '-'.join(leafs)
            else:
                module.fail_json(msg='The interface_types "switch_port", "port_channel", and "fex"                     do not support using multiple leafs for a single binding')
        else:
            module.fail_json(msg='The "leafs" parameter must not have more than 2 entries')
    interface = module.params['interface']
    extpaths = module.params['extpaths']
    state = module.params['state']
    static_path = ''
    if (encap_id is not None):
        if (encap_id in range(1, 4097)):
            encap_id = 'vlan-{0}'.format(encap_id)
        else:
            module.fail_json(msg='Valid VLAN assigments are from 1 to 4096')
    if (primary_encap_id is not None):
        if (primary_encap_id in range(1, 4097)):
            primary_encap_id = 'vlan-{0}'.format(primary_encap_id)
        else:
            module.fail_json(msg='Valid VLAN assigments are from 1 to 4096')
    INTERFACE_MODE_MAPPING = {
        '802.1p': 'native',
        'access': 'untagged',
        'native': 'native',
        'regular': 'regular',
        'tagged': 'regular',
        'trunk': 'regular',
        'untagged': 'untagged',
    }
    INTERFACE_TYPE_MAPPING = dict(fex='topology/pod-{0}/paths-{1}/extpaths-{2}/pathep-[eth{3}]'.format(pod_id, leafs, extpaths, interface), port_channel='topology/pod-{0}/paths-{1}/pathep-[{2}]'.format(pod_id, leafs, interface), switch_port='topology/pod-{0}/paths-{1}/pathep-[eth{2}]'.format(pod_id, leafs, interface), vpc='topology/pod-{0}/protpaths-{1}/pathep-[{2}]'.format(pod_id, leafs, interface))
    static_path = INTERFACE_TYPE_MAPPING[interface_type]
    path_target_filter = {
        
    }
    if ((pod_id is not None) and (leafs is not None) and (interface is not None) and ((interface_type != 'fex') or (extpaths is not None))):
        path_target_filter = {
            'tDn': static_path,
        }
    if (interface_mode is not None):
        interface_mode = INTERFACE_MODE_MAPPING[interface_mode]
    aci = ACIModule(module)
    aci.construct_url(root_class=dict(aci_class='fvTenant', aci_rn='tn-{0}'.format(tenant), module_object=tenant, target_filter={
        'name': tenant,
    }), subclass_1=dict(aci_class='fvAp', aci_rn='ap-{0}'.format(ap), module_object=ap, target_filter={
        'name': ap,
    }), subclass_2=dict(aci_class='fvAEPg', aci_rn='epg-{0}'.format(epg), module_object=epg, target_filter={
        'name': epg,
    }), subclass_3=dict(aci_class='fvRsPathAtt', aci_rn='rspathAtt-[{0}]'.format(static_path), module_object=static_path, target_filter=path_target_filter))
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='fvRsPathAtt', class_config=dict(descr=description, encap=encap_id, primaryEncap=primary_encap_id, instrImedcy=deploy_immediacy, mode=interface_mode, tDn=static_path))
        aci.get_diff(aci_class='fvRsPathAtt')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()