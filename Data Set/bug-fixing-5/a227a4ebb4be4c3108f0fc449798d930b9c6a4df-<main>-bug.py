def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(ip_address=dict(required=False), state=dict(choices=['present', 'absent'], default='present'), vpc=dict(default=None), network=dict(default=None), zone=dict(default=None), domain=dict(default=None), account=dict(default=None), project=dict(default=None), poll_async=dict(type='bool', default=True)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), required_if=[('state', 'absent', ['ip_address'])], supports_check_mode=True)
    try:
        acs_ip_address = AnsibleCloudStackIPAddress(module)
        state = module.params.get('state')
        if (state in ['absent']):
            ip_address = acs_ip_address.disassociate_ip_address()
        else:
            ip_address = acs_ip_address.associate_ip_address()
        result = acs_ip_address.get_result(ip_address)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)