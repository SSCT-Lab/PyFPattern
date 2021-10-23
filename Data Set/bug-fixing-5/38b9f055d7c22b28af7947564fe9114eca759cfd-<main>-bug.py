def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(ip_address=dict(required=True), vm=dict(default=None), vm_guest_ip=dict(default=None), network=dict(default=None), vpc=dict(default=None), state=dict(choices=['present', 'absent'], default='present'), zone=dict(default=None), domain=dict(default=None), account=dict(default=None), project=dict(default=None), poll_async=dict(type='bool', default=True)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), supports_check_mode=True)
    try:
        acs_static_nat = AnsibleCloudStackStaticNat(module)
        state = module.params.get('state')
        if (state in ['absent']):
            ip_address = acs_static_nat.absent_static_nat()
        else:
            ip_address = acs_static_nat.present_static_nat()
        result = acs_static_nat.get_result(ip_address)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)