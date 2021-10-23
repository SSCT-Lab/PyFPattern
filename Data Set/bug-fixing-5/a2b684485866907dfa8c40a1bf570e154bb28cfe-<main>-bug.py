def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True), display_text=dict(default=None), network_offering=dict(default=None), zone=dict(default=None), start_ip=dict(default=None), end_ip=dict(default=None), gateway=dict(default=None), netmask=dict(default=None), start_ipv6=dict(default=None), end_ipv6=dict(default=None), cidr_ipv6=dict(default=None), gateway_ipv6=dict(default=None), vlan=dict(default=None), vpc=dict(default=None), isolated_pvlan=dict(default=None), clean_up=dict(type='bool', default=False), network_domain=dict(default=None), state=dict(choices=['present', 'absent', 'restarted'], default='present'), acl_type=dict(choices=['account', 'domain'], default='account'), project=dict(default=None), domain=dict(default=None), account=dict(default=None), poll_async=dict(type='bool', default=True)))
    required_together = cs_required_together()
    required_together.extend([['start_ip', 'netmask', 'gateway'], ['start_ipv6', 'cidr_ipv6', 'gateway_ipv6']])
    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together, supports_check_mode=True)
    try:
        acs_network = AnsibleCloudStackNetwork(module)
        state = module.params.get('state')
        if (state in ['absent']):
            network = acs_network.absent_network()
        elif (state in ['restarted']):
            network = acs_network.restart_network()
        else:
            network = acs_network.present_network()
        result = acs_network.get_result(network)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)