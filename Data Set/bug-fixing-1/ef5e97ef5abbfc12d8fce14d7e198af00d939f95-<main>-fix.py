

def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(tenant=dict(type='str', aliases=['tenant_name']), ap=dict(type='str', aliases=['app_profile', 'app_profile_name']), epg=dict(type='str', aliases=['epg_name']), encap_id=dict(type='int', aliases=['vlan', 'vlan_id']), primary_encap_id=dict(type='int', aliases=['primary_vlan', 'primary_vlan_id']), deploy_immediacy=dict(type='str', choices=['immediate', 'lazy']), interface_mode=dict(type='str', choices=['untagged', '802.1p', 'trunk', 'regular', 'native', 'tagged', 'access'], aliases=['mode', 'interface_mode_name']), interface_type=dict(type='str', choices=['switch_port', 'vpc', 'port_channel', 'fex'], required=True), pod=dict(type='int', aliases=['pod_number']), leafs=dict(type='list', aliases=['paths', 'leaves', 'nodes', 'switches']), interface=dict(type='str'), extpaths=dict(type='int'), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['tenant', 'ap', 'epg', 'interface_type', 'pod', 'leafs', 'interface']], ['state', 'present', ['tenant', 'ap', 'epg', 'encap_id', 'interface_type', 'pod', 'leafs', 'interface']], ['interface_type', 'fex', ['extpaths']]])
    tenant = module.params['tenant']
    ap = module.params['ap']
    epg = module.params['epg']
    encap_id = module.params['encap_id']
    primary_encap_id = module.params['primary_encap_id']
    deploy_immediacy = module.params['deploy_immediacy']
    interface_mode = module.params['interface_mode']
    interface_type = module.params['interface_type']
    pod = module.params['pod']
    leafs = [str(leaf) for leaf in module.params['leafs']]
    if (leafs is not None):
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
        'access': 'untagged',
        'untagged': 'untagged',
        'tagged': 'regular',
        'trunk': 'regular',
        'regular': 'regular',
        '802.1p': 'native',
        'native': 'native',
    }
    INTERFACE_TYPE_MAPPING = dict(switch_port='topology/pod-{0}/paths-{1}/pathep-[eth{2}]'.format(pod, leafs, interface), port_channel='topology/pod-{0}/paths-{1}/pathep-[eth{2}]'.format(pod, leafs, interface), vpc='topology/pod-{0}/protpaths-{1}/pathep-[{2}]'.format(pod, leafs, interface), fex='topology/pod-{0}/paths-{1}/extpaths-{2}/pathep-[eth{3}]'.format(pod, leafs, extpaths, interface))
    static_path = INTERFACE_TYPE_MAPPING[interface_type]
    if (interface_mode is not None):
        interface_mode = INTERFACE_MODE_MAPPING[interface_mode]
    aci = ACIModule(module)
    aci.construct_url(root_class=dict(aci_class='fvTenant', aci_rn='tn-{0}'.format(tenant), filter_target='eq(fvTenant.name, "{0}")'.format(tenant), module_object=tenant), subclass_1=dict(aci_class='fvAp', aci_rn='ap-{0}'.format(ap), filter_target='eq(fvAp.name, "{0}")'.format(ap), module_object=ap), subclass_2=dict(aci_class='fvAEPg', aci_rn='epg-{0}'.format(epg), filter_target='eq(fvAEPg.name, "{0}")'.format(epg), module_object=epg), subclass_3=dict(aci_class='fvRsPathAtt', aci_rn='rspathAtt-[{0}]'.format(static_path), filter_target='eq(fvRsPathAtt.tDn, "{0}"'.format(static_path), module_object=static_path))
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='fvRsPathAtt', class_config=dict(encap=encap_id, primaryEncap=primary_encap_id, instrImedcy=deploy_immediacy, mode=interface_mode, tDn=static_path))
        aci.get_diff(aci_class='fvRsPathAtt')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    module.exit_json(**aci.result)
