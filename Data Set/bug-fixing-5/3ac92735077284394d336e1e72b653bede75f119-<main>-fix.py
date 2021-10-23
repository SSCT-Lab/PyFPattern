def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(default='present', choices=['present', 'absent']), name=dict(required=True, type='str'), hash_key_name=dict(type='str'), hash_key_type=dict(default='STRING', type='str', choices=['STRING', 'NUMBER', 'BINARY']), range_key_name=dict(type='str'), range_key_type=dict(default='STRING', type='str', choices=['STRING', 'NUMBER', 'BINARY']), read_capacity=dict(default=1, type='int'), write_capacity=dict(default=1, type='int'), indexes=dict(default=[], type='list'), tags=dict(type='dict'), wait_for_active_timeout=dict(default=60, type='int')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    if ((not HAS_BOTO3) and module.params.get('tags')):
        module.fail_json(msg='boto3 required when using tags for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if (not region):
        module.fail_json(msg='region must be specified')
    try:
        connection = connect_to_aws(boto.dynamodb2, region, **aws_connect_params)
    except (NoAuthHandlerFound, AnsibleAWSError) as e:
        module.fail_json(msg=str(e))
    if module.params.get('tags'):
        try:
            (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
            boto3_dynamodb = boto3_conn(module, conn_type='client', resource='dynamodb', region=region, endpoint=ec2_url, **aws_connect_kwargs)
            if (not hasattr(boto3_dynamodb, 'tag_resource')):
                module.fail_json(msg='boto3 connection does not have tag_resource(), likely due to using an old version')
            boto3_sts = boto3_conn(module, conn_type='client', resource='sts', region=region, endpoint=ec2_url, **aws_connect_kwargs)
        except botocore.exceptions.NoCredentialsError as e:
            module.fail_json(msg='cannot connect to AWS', exception=traceback.format_exc(e))
    else:
        boto3_dynamodb = None
        boto3_sts = None
    state = module.params.get('state')
    if (state == 'present'):
        create_or_update_dynamo_table(connection, module, boto3_dynamodb, boto3_sts)
    elif (state == 'absent'):
        delete_dynamo_table(connection, module)