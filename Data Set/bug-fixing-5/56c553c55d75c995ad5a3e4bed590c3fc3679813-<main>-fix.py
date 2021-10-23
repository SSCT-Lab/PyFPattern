def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True, aliases=['physical_network']), zone=dict(), domain=dict(), vlan=dict(), nsps_disabled=dict(type='list'), nsps_enabled=dict(type='list'), network_speed=dict(choices=['1G', '10G']), broadcast_domain_range=dict(choices=['POD', 'ZONE']), isolation_method=dict(choices=['VLAN', 'GRE', 'L3']), state=dict(choices=['present', 'enabled', 'disabled', 'absent'], default='present'), tags=dict(aliases=['tag']), poll_async=dict(type='bool', default=True)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), supports_check_mode=True)
    acs_network = AnsibleCloudStackPhysicalNetwork(module)
    state = module.params.get('state')
    nsps_disabled = module.params.get('nsps_disabled', [])
    nsps_enabled = module.params.get('nsps_enabled', [])
    if (state in ['absent']):
        network = acs_network.absent_network()
    else:
        network = acs_network.present_network()
    if (nsps_disabled is not None):
        for name in nsps_disabled:
            acs_network.update_nsp(name=name, state='Disabled')
    if (nsps_enabled is not None):
        for nsp_name in nsps_enabled:
            if (nsp_name.lower() in ['virtualrouter', 'vpcvirtualrouter']):
                acs_network.set_vrouter_element_state(enabled=True, nsp_name=nsp_name)
            elif (nsp_name.lower() == 'internallbvm'):
                acs_network.set_loadbalancer_element_state(enabled=True, nsp_name=nsp_name)
            acs_network.update_nsp(name=nsp_name, state='Enabled')
    result = acs_network.get_result(network)
    if nsps_enabled:
        result['nsps_enabled'] = nsps_enabled
    if nsps_disabled:
        result['nsps_disabled'] = nsps_disabled
    module.exit_json(**result)