

def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(policy_group=dict(type='str', aliases=['name', 'policy_group_name']), description=dict(type='str', aliases=['descr']), lag_type=dict(type='str', aliases=['lag_type_name'], choices=['leaf', 'link', 'node']), link_level_policy=dict(type='str', aliases=['link_level_policy_name']), cdp_policy=dict(type='str', aliases=['cdp_policy_name']), mcp_policy=dict(type='str', aliases=['mcp_policy_name']), lldp_policy=dict(type='str', aliases=['lldp_policy_name']), stp_interface_policy=dict(type='str', aliases=['stp_interface_policy_name']), egress_data_plane_policing_policy=dict(type='str', aliases=['egress_data_plane_policing_policy_name']), ingress_data_plane_policing_policy=dict(type='str', aliases=['ingress_data_plane_policing_policy_name']), priority_flow_control_policy=dict(type='str', aliases=['priority_flow_control_policy_name']), fibre_channel_interface_policy=dict(type='str', aliases=['fibre_channel_interface_policy_name']), slow_drain_policy=dict(type='str', aliases=['slow_drain_policy_name']), port_channel_policy=dict(type='str', aliases=['port_channel_policy_name']), monitoring_policy=dict(type='str', aliases=['monitoring_policy_name']), storm_control_interface_policy=dict(type='str', aliases=['storm_control_interface_policy_name']), l2_interface_policy=dict(type='str', aliases=['l2_interface_policy_name']), port_security_policy=dict(type='str', aliases=['port_security_policy_name']), aep=dict(type='str', aliases=['aep_name']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['lag_type', 'policy_group']], ['state', 'present', ['lag_type', 'policy_group']]])
    policy_group = module.params['policy_group']
    description = module.params['description']
    lag_type = module.params['lag_type']
    link_level_policy = module.params['link_level_policy']
    cdp_policy = module.params['cdp_policy']
    mcp_policy = module.params['mcp_policy']
    lldp_policy = module.params['lldp_policy']
    stp_interface_policy = module.params['stp_interface_policy']
    egress_data_plane_policing_policy = module.params['egress_data_plane_policing_policy']
    ingress_data_plane_policing_policy = module.params['ingress_data_plane_policing_policy']
    priority_flow_control_policy = module.params['priority_flow_control_policy']
    fibre_channel_interface_policy = module.params['fibre_channel_interface_policy']
    slow_drain_policy = module.params['slow_drain_policy']
    port_channel_policy = module.params['port_channel_policy']
    monitoring_policy = module.params['monitoring_policy']
    storm_control_interface_policy = module.params['storm_control_interface_policy']
    l2_interface_policy = module.params['l2_interface_policy']
    port_security_policy = module.params['port_security_policy']
    aep = module.params['aep']
    state = module.params['state']
    if (lag_type == 'leaf'):
        aci_class_name = 'infraAccPortGrp'
        dn_name = 'accportgrp'
        class_config_dict = dict(name=policy_group, descr=description)
    elif ((lag_type == 'link') or (lag_type == 'node')):
        aci_class_name = 'infraAccBndlGrp'
        dn_name = 'accbundle'
        class_config_dict = dict(name=policy_group, descr=description, lagT=lag_type)
    aci = ACIModule(module)
    aci.construct_url(root_class=dict(aci_class=aci_class_name, aci_rn='infra/funcprof/{0}-{1}'.format(dn_name, policy_group), filter_target='eq({0}.name, "{1}")'.format(aci_class_name, policy_group), module_object=policy_group), child_classes=['infraRsAttEntP', 'infraRsCdpIfPol', 'infraRsFcIfPol', 'infraRsHIfPol', 'infraRsL2IfPol', 'infraRsL2PortSecurityPol', 'infraRsLacpPol', 'infraRsLldpIfPol', 'infraRsMcpIfPol', 'infraRsMonIfInfraPol', 'infraRsQosEgressDppIfPol', 'infraRsQosIngressDppIfPol', 'infraRsQosPfcIfPol', 'infraRsQosSdIfPol', 'infraRsStormctrlIfPol', 'infraRsStpIfPol'])
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class=aci_class_name, class_config=class_config_dict, child_configs=[dict(infraRsAttEntP=dict(attributes=dict(tDn='uni/infra/attentp-{0}'.format(aep)))), dict(infraRsCdpIfPol=dict(attributes=dict(tnCdpIfPolName=cdp_policy))), dict(infraRsFcIfPol=dict(attributes=dict(tnFcIfPolName=fibre_channel_interface_policy))), dict(infraRsHIfPol=dict(attributes=dict(tnFabricHIfPolName=link_level_policy))), dict(infraRsL2IfPol=dict(attributes=dict(tnL2IfPolName=l2_interface_policy))), dict(infraRsL2PortSecurityPol=dict(attributes=dict(tnL2PortSecurityPolName=port_security_policy))), dict(infraRsLacpPol=dict(attributes=dict(tnLacpLagPolName=port_channel_policy))), dict(infraRsLldpIfPol=dict(attributes=dict(tnLldpIfPolName=lldp_policy))), dict(infraRsMcpIfPol=dict(attributes=dict(tnMcpIfPolName=mcp_policy))), dict(infraRsMonIfInfraPol=dict(attributes=dict(tnMonInfraPolName=monitoring_policy))), dict(infraRsQosEgressDppIfPol=dict(attributes=dict(tnQosDppPolName=egress_data_plane_policing_policy))), dict(infraRsQosIngressDppIfPol=dict(attributes=dict(tnQosDppPolName=ingress_data_plane_policing_policy))), dict(infraRsQosPfcIfPol=dict(attributes=dict(tnQosPfcIfPolName=priority_flow_control_policy))), dict(infraRsQosSdIfPol=dict(attributes=dict(tnQosSdIfPolName=slow_drain_policy))), dict(infraRsStormctrlIfPol=dict(attributes=dict(tnStormctrlIfPolName=storm_control_interface_policy))), dict(infraRsStpIfPol=dict(attributes=dict(tnStpIfPolName=stp_interface_policy)))])
        aci.get_diff(aci_class=aci_class_name)
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()
