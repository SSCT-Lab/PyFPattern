

def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(bd=dict(type='str', aliases=['bd_name']), description=dict(type='str', aliases=['descr']), enable_vip=dict(type='bool'), gateway=dict(type='str', aliases=['gateway_ip']), mask=dict(type='int', aliases=['subnet_mask']), subnet_name=dict(type='str', aliases=['name']), nd_prefix_policy=dict(type='str'), preferred=dict(type='bool'), route_profile=dict(type='str'), route_profile_l3_out=dict(type='str'), scope=dict(type='list', choices=['private', 'public', 'shared']), subnet_control=dict(type='str', choices=['nd_ra', 'no_gw', 'querier_ip', 'unspecified']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']), tenant=dict(type='str', aliases=['tenant_name']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_together=[['gateway', 'mask']], required_if=[['state', 'present', ['bd', 'gateway', 'mask', 'tenant']], ['state', 'absent', ['bd', 'gateway', 'mask', 'tenant']]])
    aci = ACIModule(module)
    description = module.params['description']
    enable_vip = aci.boolean(module.params['enable_vip'])
    tenant = module.params['tenant']
    bd = module.params['bd']
    gateway = module.params['gateway']
    mask = module.params['mask']
    if ((mask is not None) and (mask not in range(0, 129))):
        module.fail_json(msg='Valid Subnet Masks are 0 to 32 for IPv4 Addresses and 0 to 128 for IPv6 addresses')
    if (gateway is not None):
        gateway = '{0}/{1}'.format(gateway, str(mask))
    subnet_name = module.params['subnet_name']
    nd_prefix_policy = module.params['nd_prefix_policy']
    preferred = aci.boolean(module.params['preferred'])
    route_profile = module.params['route_profile']
    route_profile_l3_out = module.params['route_profile_l3_out']
    scope = module.params['scope']
    if (scope is not None):
        if (('private' in scope) and ('public' in scope)):
            module.fail_json(msg=("Parameter 'scope' cannot be both 'private' and 'public', got: %s" % scope))
        else:
            scope = ','.join(sorted(scope))
    state = module.params['state']
    subnet_control = module.params['subnet_control']
    if subnet_control:
        subnet_control = SUBNET_CONTROL_MAPPING[subnet_control]
    aci.construct_url(root_class=dict(aci_class='fvTenant', aci_rn='tn-{0}'.format(tenant), filter_target='eq(fvTenant.name, "{0}")'.format(tenant), module_object=tenant), subclass_1=dict(aci_class='fvBD', aci_rn='BD-{0}'.format(bd), filter_target='eq(fvBD.name, "{0}")'.format(bd), module_object=bd), subclass_2=dict(aci_class='fvSubnet', aci_rn='subnet-[{0}]'.format(gateway), filter_target='eq(fvSubnet.ip, "{0}")'.format(gateway), module_object=gateway), child_classes=['fvRsBDSubnetToProfile', 'fvRsNdPfxPol'])
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='fvSubnet', class_config=dict(ctrl=subnet_control, descr=description, ip=gateway, name=subnet_name, preferred=preferred, scope=scope, virtual=enable_vip), child_configs=[{
            'fvRsBDSubnetToProfile': {
                'attributes': {
                    'tnL3extOutName': route_profile_l3_out,
                    'tnRtctrlProfileName': route_profile,
                },
            },
        }, {
            'fvRsNdPfxPol': {
                'attributes': {
                    'tnNdPfxPolName': nd_prefix_policy,
                },
            },
        }])
        aci.get_diff(aci_class='fvSubnet')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()
