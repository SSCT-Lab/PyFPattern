

def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(domain=dict(type='str', aliases=['domain_name', 'domain_profile']), domain_type=dict(type='str', choices=['fc', 'l2dom', 'l3dom', 'phys', 'vmm']), pool=dict(type='str', aliases=['pool_name', 'vlan_pool']), pool_allocation_mode=dict(type='str', required=True, aliases=['allocation_mode', 'mode'], choices=['dynamic', 'static']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']), vm_provider=dict(type='str', choices=['cloudfoundry', 'kubernetes', 'microsoft', 'openshift', 'openstack', 'redhat', 'vmware']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['domain_type', 'vmm', ['vm_provider']], ['state', 'absent', ['domain', 'domain_type', 'pool']], ['state', 'present', ['domain', 'domain_type', 'pool']]])
    domain = module.params['domain']
    domain_type = module.params['domain_type']
    pool = module.params['pool']
    pool_allocation_mode = module.params['pool_allocation_mode']
    vm_provider = module.params['vm_provider']
    state = module.params['state']
    if ((domain_type != 'vmm') and (vm_provider is not None)):
        module.fail_json(msg="Domain type '{0}' cannot have a 'vm_provider'".format(domain_type))
    pool_name = pool
    if (pool is not None):
        pool_name = '[{0}]-{1}'.format(pool, pool_allocation_mode)
    if (domain_type == 'fc'):
        domain_class = 'fcDomP'
        domain_mo = 'uni/fc-{0}'.format(domain)
        domain_rn = 'fc-{0}'.format(domain)
    elif (domain_type == 'l2dom'):
        domain_class = 'l2extDomP'
        domain_mo = 'uni/l2dom-{0}'.format(domain)
        domain_rn = 'l2dom-{0}'.format(domain)
    elif (domain_type == 'l3dom'):
        domain_class = 'l3extDomP'
        domain_mo = 'uni/l3dom-{0}'.format(domain)
        domain_rn = 'l3dom-{0}'.format(domain)
    elif (domain_type == 'phys'):
        domain_class = 'physDomP'
        domain_mo = 'uni/phys-{0}'.format(domain)
        domain_rn = 'phys-{0}'.format(domain)
    elif (domain_type == 'vmm'):
        domain_class = 'vmmDomP'
        domain_mo = 'uni/vmmp-{0}/dom-{1}'.format(VM_PROVIDER_MAPPING[vm_provider], domain)
        domain_rn = 'dom-{0}'.format(domain)
    aci_mo = ('uni/infra/vlanns-' + pool_name)
    aci = ACIModule(module)
    aci.construct_url(root_class=dict(aci_class=domain_class, aci_rn=domain_rn, filter_target='eq({0}.name, "{1}")'.format(domain_class, domain), module_object=domain_mo), child_classes=['infraRsVlanNs'])
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class=domain_class, class_config=dict(name=domain), child_configs=[{
            'infraRsVlanNs': {
                'attributes': {
                    'tDn': aci_mo,
                },
            },
        }])
        aci.get_diff(aci_class=domain_class)
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()
