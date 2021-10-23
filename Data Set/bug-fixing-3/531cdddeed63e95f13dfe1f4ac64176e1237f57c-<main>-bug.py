def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(filters=dict(type='dict', default=dict()), internet_gateway_ids=dict(type='list', default=None)))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='botocore and boto3 are required.')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=("Can't authorize connection - " + str(e)))
    results = list_internet_gateways(connection, module)
    module.exit_json(result=results)