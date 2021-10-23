def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(ip_address=dict(required=True), vm=dict(), vm_guest_ip=dict(), network=dict(), vpc=dict(), state=dict(choices=['present', 'absent'], default='present'), zone=dict(), domain=dict(), account=dict(), project=dict(), poll_async=dict(type='bool', default=True)))
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