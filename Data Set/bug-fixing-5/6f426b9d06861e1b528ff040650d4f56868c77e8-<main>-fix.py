def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True), cidr=dict(default=None), display_text=dict(default=None), vpc_offering=dict(default=None), network_domain=dict(default=None), state=dict(choices=['present', 'absent', 'restarted'], default='present'), domain=dict(default=None), account=dict(default=None), project=dict(default=None), zone=dict(default=None), tags=dict(type='list', aliases=['tag'], default=None), poll_async=dict(type='bool', default=True)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), required_if=[('state', 'present', ['cidr'])], supports_check_mode=True)
    try:
        acs_vpc = AnsibleCloudStackVpc(module)
        state = module.params.get('state')
        if (state == 'absent'):
            vpc = acs_vpc.absent_vpc()
        elif (state == 'restarted'):
            vpc = acs_vpc.restart_vpc()
        else:
            vpc = acs_vpc.present_vpc()
        result = acs_vpc.get_result(vpc)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)