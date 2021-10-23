def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True), display_text=dict(), network_offering=dict(), zone=dict(), start_ip=dict(), end_ip=dict(), gateway=dict(), netmask=dict(), start_ipv6=dict(), end_ipv6=dict(), cidr_ipv6=dict(), gateway_ipv6=dict(), vlan=dict(), vpc=dict(), isolated_pvlan=dict(), clean_up=dict(type='bool', default=False), network_domain=dict(), state=dict(choices=['present', 'absent', 'restarted'], default='present'), acl_type=dict(choices=['account', 'domain']), project=dict(), domain=dict(), account=dict(), poll_async=dict(type='bool', default=True)))
    required_together = cs_required_together()
    required_together.extend([['netmask', 'gateway']])
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