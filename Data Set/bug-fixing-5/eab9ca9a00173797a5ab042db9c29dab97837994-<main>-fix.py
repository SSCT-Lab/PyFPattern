def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(vpc_id=dict(), service=dict(), policy=dict(type='json'), policy_file=dict(type='path', aliases=['policy_path']), state=dict(default='present', choices=['present', 'absent']), wait=dict(type='bool', default=False), wait_timeout=dict(type='int', default=320, required=False), route_table_ids=dict(type='list'), vpc_endpoint_id=dict(), client_token=dict()))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=[['policy', 'policy_file']], required_if=[['state', 'present', ['vpc_id', 'service']], ['state', 'absent', ['vpc_endpoint_id']]])
    if (not HAS_BOTO3):
        module.fail_json(msg='botocore and boto3 are required for this module')
    state = module.params.get('state')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    except NameError as e:
        if ("global name 'boto' is not defined" in e.message):
            module.params['region'] = botocore.session.get_session().get_config_variable('region')
            if (not module.params['region']):
                module.fail_json(msg='Error - no region provided')
        else:
            module.fail_json(msg=("Can't retrieve connection information - " + str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        ec2 = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=('Failed to connect to AWS due to wrong or missing credentials: %s' % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    if (state == 'present'):
        (changed, results) = setup_creation(ec2, module)
    else:
        (changed, results) = setup_removal(ec2, module)
    module.exit_json(changed=changed, result=results)