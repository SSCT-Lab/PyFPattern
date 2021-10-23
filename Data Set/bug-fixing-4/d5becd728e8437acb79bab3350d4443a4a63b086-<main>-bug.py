def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True, aliases=['url']), password=dict(default=None, no_log=True), username=dict(default=None), hypervisor=dict(choices=CS_HYPERVISORS, default=None), allocation_state=dict(default=None), pod=dict(default=None), cluster=dict(default=None), host_tags=dict(default=None, type='list'), zone=dict(default=None), state=dict(choices=['present', 'absent'], default='present')))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), supports_check_mode=True)
    try:
        acs_host = AnsibleCloudStackHost(module)
        state = module.params.get('state')
        if (state == 'absent'):
            host = acs_host.absent_host()
        else:
            host = acs_host.present_host()
        result = acs_host.get_result(host)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)