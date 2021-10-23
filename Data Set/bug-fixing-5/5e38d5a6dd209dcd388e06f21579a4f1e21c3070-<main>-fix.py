def main():
    '\n    Main entry point.\n\n    :return dict: ansible facts\n    '
    argument_spec = dict(function_name=dict(required=False, default=None, aliases=['function', 'name']), query=dict(required=False, choices=['aliases', 'all', 'config', 'mappings', 'policy', 'versions'], default='all'), event_source_arn=dict(required=False, default=None))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=[], required_together=[])
    function_name = module.params['function_name']
    if function_name:
        if (not re.search('^[\\w\\-:]+$', function_name)):
            module.fail_json(msg='Function name {0} is invalid. Names must contain only alphanumeric characters and hyphens.'.format(function_name))
        if (len(function_name) > 64):
            module.fail_json(msg='Function name "{0}" exceeds 64 character limit'.format(function_name))
    try:
        (region, endpoint, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        aws_connect_kwargs.update(dict(region=region, endpoint=endpoint, conn_type='client', resource='lambda'))
        client = boto3_conn(module, **aws_connect_kwargs)
    except ClientError as e:
        module.fail_json_aws(e, 'trying to set up boto connection')
    invocations = dict(aliases='alias_details', all='all_details', config='config_details', mappings='mapping_details', policy='policy_details', versions='version_details')
    this_module_function = globals()[invocations[module.params['query']]]
    all_facts = fix_return(this_module_function(client, module))
    results = dict(function=all_facts, changed=False)
    if module.check_mode:
        results['msg'] = 'Check mode set but ignored for fact gathering only.'
    module.exit_json(**results)