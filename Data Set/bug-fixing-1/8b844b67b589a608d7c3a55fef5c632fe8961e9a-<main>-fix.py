

def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(tenant=dict(type='str', aliases=['tenant_name']), l3out=dict(type='str', aliases=['l3out_name', 'name']), domain=dict(type='str', aliases=['ext_routed_domain_name', 'routed_domain']), vrf=dict(type='str', aliases=['vrf_name']), description=dict(type='str', aliases=['descr']), route_control=dict(type='list', choices=['export', 'import'], aliases=['route_control_enforcement']), dscp=dict(type='str', choices=['AF11', 'AF12', 'AF13', 'AF21', 'AF22', 'AF23', 'AF31', 'AF32', 'AF33', 'AF41', 'AF42', 'AF43', 'CS0', 'CS1', 'CS2', 'CS3', 'CS4', 'CS5', 'CS6', 'CS7', 'EF', 'VA', 'unspecified'], aliases=['target']), l3protocol=dict(type='list', choices=['bgp', 'eigrp', 'ospf', 'pim', 'static']), asn=dict(type='int', aliases=['as_number']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['l3out', 'tenant']], ['state', 'present', ['l3out', 'tenant', 'domain', 'vrf']]])
    aci = ACIModule(module)
    l3out = module.params['l3out']
    domain = module.params['domain']
    dscp = module.params['dscp']
    description = module.params['description']
    enforceRtctrl = module.params['route_control']
    vrf = module.params['vrf']
    l3protocol = module.params['l3protocol']
    asn = module.params['asn']
    state = module.params['state']
    tenant = module.params['tenant']
    if l3protocol:
        if (('eigrp' in l3protocol) and (asn is None)):
            module.fail_json(msg="Parameter 'asn' is required when l3protocol is 'eigrp'")
        if (('eigrp' not in l3protocol) and (asn is not None)):
            module.warn("Parameter 'asn' is only applicable when l3protocol is 'eigrp'. The ASN will be ignored")
    enforce_ctrl = ''
    if (enforceRtctrl is not None):
        if ((len(enforceRtctrl) == 1) and (enforceRtctrl[0] == 'import')):
            aci.fail_json('The route_control parameter is invalid: allowed options are export or import,export only')
        elif ((len(enforceRtctrl) == 1) and (enforceRtctrl[0] == 'export')):
            enforce_ctrl = 'export'
        else:
            enforce_ctrl = 'export,import'
    child_classes = ['l3extRsL3DomAtt', 'l3extRsEctx', 'bgpExtP', 'ospfExtP', 'eigrpExtP', 'pimExtP']
    aci.construct_url(root_class=dict(aci_class='fvTenant', aci_rn='tn-{0}'.format(tenant), module_object=tenant, target_filter={
        'name': tenant,
    }), subclass_1=dict(aci_class='l3extOut', aci_rn='out-{0}'.format(l3out), module_object=l3out, target_filter={
        'name': l3out,
    }), child_classes=child_classes)
    aci.get_existing()
    child_configs = [dict(l3extRsL3DomAtt=dict(attributes=dict(tDn='uni/l3dom-{0}'.format(domain)))), dict(l3extRsEctx=dict(attributes=dict(tnFvCtxName=vrf)))]
    if (l3protocol is not None):
        for protocol in l3protocol:
            if (protocol == 'bgp'):
                child_configs.append(dict(bgpExtP=dict(attributes=dict(descr='', nameAlias=''))))
            elif (protocol == 'eigrp'):
                child_configs.append(dict(eigrpExtP=dict(attributes=dict(descr='', nameAlias='', asn=asn))))
            elif (protocol == 'ospf'):
                child_configs.append(dict(ospfExtP=dict(attributes=dict(descr='', nameAlias=''))))
            elif (protocol == 'pim'):
                child_configs.append(dict(pimExtP=dict(attributes=dict(descr='', nameAlias=''))))
    if (state == 'present'):
        aci.payload(aci_class='l3extOut', class_config=dict(name=l3out, descr=description, dn='uni/tn-{0}/out-{1}'.format(tenant, l3out), enforceRtctrl=enforce_ctrl, targetDscp=dscp), child_configs=child_configs)
        aci.get_diff(aci_class='l3extOut')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()
