def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(resource_type=dict(required=True, choices=RESOURCE_TYPES.keys(), aliases=['type']), limit=dict(default=(- 1), aliases=['max'], type='int'), domain=dict(default=None), account=dict(default=None), project=dict(default=None)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), supports_check_mode=True)
    try:
        acs_resource_limit = AnsibleCloudStackResourceLimit(module)
        resource_limit = acs_resource_limit.update_resource_limit()
        result = acs_resource_limit.get_result(resource_limit)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)