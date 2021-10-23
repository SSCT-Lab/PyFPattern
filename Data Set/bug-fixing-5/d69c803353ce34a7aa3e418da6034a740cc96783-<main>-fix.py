def main():
    argument_spec = aci_argument_spec
    argument_spec.update(allow_useg=dict(type='str', choices=['encap', 'useg']), ap=dict(type='str', aliases=['app_profile', 'app_profile_name']), deploy_immediacy=dict(type='str', choices=['immediate', 'on-demand']), domain=dict(type='str', aliases=['domain_name', 'domain_profile']), domain_type=dict(type='str', choices=['phys', 'vmm'], aliases=['type']), encap=dict(type='int'), encap_mode=dict(type='str', choices=['auto', 'vlan', 'vxlan']), epg=dict(type='str', aliases=['name', 'epg_name']), netflow=dict(type='str', choices=['disabled', 'enabled']), primary_encap=dict(type='int'), resolution_immediacy=dict(type='str', choices=['immediate', 'lazy', 'pre-provision']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']), tenant=dict(type='str', aliases=['tenant_name']), vm_provider=dict(type='str', choices=['vmware']), method=dict(type='str', choices=['delete', 'get', 'post'], aliases=['action'], removed_in_version='2.6'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['domain_type', 'vmm', ['vm_provider']], ['state', 'absent', ['ap', 'domain', 'domain_type', 'epg', 'tenant']], ['state', 'present', ['ap', 'domain', 'domain_type', 'epg', 'tenant']]])
    allow_useg = module.params['allow_useg']
    deploy_immediacy = module.params['deploy_immediacy']
    domain = module.params['domain']
    domain_type = module.params['domain_type']
    vm_provider = module.params['vm_provider']
    encap = module.params['encap']
    if (encap is not None):
        if (encap in range(1, 4097)):
            encap = 'vlan-{}'.format(encap)
        else:
            module.fail_json(msg='Valid VLAN assigments are from 1 to 4096')
    encap_mode = module.params['encap_mode']
    netflow = module.params['netflow']
    primary_encap = module.params['primary_encap']
    if (primary_encap is not None):
        if (primary_encap in range(1, 4097)):
            primary_encap = 'vlan-{}'.format(primary_encap)
        else:
            module.fail_json(msg='Valid VLAN assigments are from 1 to 4096')
    resolution_immediacy = module.params['resolution_immediacy']
    state = module.params['state']
    if ((domain_type == 'phys') and (vm_provider is not None)):
        module.fail_json(msg="Domain type 'phys' cannot have a 'vm_provider'")
    if (domain_type == 'vmm'):
        module.params['epg_domain'] = (VM_PROVIDER_MAPPING[vm_provider] + domain)
    elif (domain_type is not None):
        module.params['epg_domain'] = ('uni/phys-' + domain)
    aci = ACIModule(module)
    aci.construct_url(root_class='tenant', subclass_1='ap', subclass_2='epg', subclass_3='epg_domain')
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='fvRsDomAtt', class_config=dict(classPref=allow_useg, encap=encap, encapMode=encap_mode, instrImedcy=deploy_immediacy, netflowPref=netflow, primaryEncap=primary_encap, resImedcy=resolution_immediacy))
        aci.get_diff(aci_class='fvRsDomAtt')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    module.params.pop('epg_domain')
    module.exit_json(**aci.result)