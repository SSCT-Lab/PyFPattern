

def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(id=dict(default=None), name=dict(required=True), dns1=dict(default=None), dns2=dict(default=None), internal_dns1=dict(default=None), internal_dns2=dict(default=None), dns1_ipv6=dict(default=None), dns2_ipv6=dict(default=None), network_type=dict(default='basic', choices=['Basic', 'basic', 'Advanced', 'advanced']), network_domain=dict(default=None), guest_cidr_address=dict(default=None), dhcp_provider=dict(default=None), local_storage_enabled=dict(default=None), securitygroups_enabled=dict(default=None), state=dict(choices=['present', 'enabled', 'disabled', 'absent'], default='present'), domain=dict(default=None)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), supports_check_mode=True)
    try:
        acs_zone = AnsibleCloudStackZone(module)
        state = module.params.get('state')
        if (state in ['absent']):
            zone = acs_zone.absent_zone()
        else:
            zone = acs_zone.present_zone()
        result = acs_zone.get_result(zone)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)
