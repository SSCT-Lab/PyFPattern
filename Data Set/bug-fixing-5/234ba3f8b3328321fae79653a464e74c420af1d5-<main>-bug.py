def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(vpc_ids=dict(type='list', default=[]), filters=dict(type='dict', default={
        
    })))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 and botocore are required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if region:
        try:
            connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
        except (botocore.exceptions.NoCredentialsError, botocore.exceptions.ProfileNotFound) as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    else:
        module.fail_json(msg='region must be specified')
    describe_vpcs(connection, module)