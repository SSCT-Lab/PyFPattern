def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(az=dict(default=None, required=False), cidr=dict(default=None, required=True), state=dict(default='present', choices=['present', 'absent']), tags=dict(default={
        
    }, required=False, type='dict', aliases=['resource_tags']), vpc_id=dict(default=None, required=True), map_public=dict(default=False, required=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 and botocore are required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if region:
        connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        module.fail_json(msg='region must be specified')
    vpc_id = module.params.get('vpc_id')
    tags = module.params.get('tags')
    cidr = module.params.get('cidr')
    az = module.params.get('az')
    state = module.params.get('state')
    map_public = module.params.get('map_public')
    try:
        if (state == 'present'):
            result = ensure_subnet_present(connection, module, vpc_id, cidr, az, tags, map_public, check_mode=module.check_mode)
        elif (state == 'absent'):
            result = ensure_subnet_absent(connection, module, vpc_id, cidr, check_mode=module.check_mode)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    module.exit_json(**result)