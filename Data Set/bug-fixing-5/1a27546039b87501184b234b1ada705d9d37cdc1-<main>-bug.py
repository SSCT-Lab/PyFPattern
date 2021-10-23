def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True), service_offering=dict(), state=dict(choices=['present', 'started', 'stopped', 'restarted', 'absent'], default='present'), domain=dict(), account=dict(), project=dict(), zone=dict(), poll_async=dict(type='bool', default=True)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), supports_check_mode=True)
    try:
        acs_router = AnsibleCloudStackRouter(module)
        state = module.params.get('state')
        if (state in ['absent']):
            router = acs_router.absent_router()
        else:
            router = acs_router.present_router()
        result = acs_router.get_result(router)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)