def main():
    'Produce a list of function suffixes which handle lambda events.'
    this_module = sys.modules[__name__]
    source_choices = ['stream']
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=False, default='present', choices=['present', 'absent']), lambda_function_arn=dict(required=True, default=None, aliases=['function_name', 'function_arn']), event_source=dict(required=False, default='stream', choices=source_choices), source_params=dict(type='dict', required=True, default=None), alias=dict(required=False, default=None), version=dict(type='int', required=False, default=0)))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=[['alias', 'version']], required_together=[])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required for this module.')
    aws = AWSConnection(module, ['lambda'])
    validate_params(module, aws)
    this_module_function = getattr(this_module, 'lambda_event_{0}'.format(module.params['event_source'].lower()))
    results = this_module_function(module, aws)
    module.exit_json(**results)