def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(az=dict(default=None, required=False), cidr=dict(default=None, required=True), ipv6_cidr=dict(default='', required=False), state=dict(default='present', choices=['present', 'absent']), tags=dict(default={
        
    }, required=False, type='dict', aliases=['resource_tags']), vpc_id=dict(default=None, required=True), map_public=dict(default=False, required=False, type='bool'), assign_instances_ipv6=dict(default=False, required=False, type='bool'), wait=dict(type='bool', default=True), wait_timeout=dict(type='int', default=300, required=False), purge_tags=dict(default=True, type='bool')))
    required_if = [('assign_instances_ipv6', True, ['ipv6_cidr'])]
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)
    if (module.params.get('assign_instances_ipv6') and (not module.params.get('ipv6_cidr'))):
        module.fail_json(msg='assign_instances_ipv6 is True but ipv6_cidr is None or an empty string')
    if (LooseVersion(botocore.__version__) < '1.7.0'):
        module.warn('botocore >= 1.7.0 is required to use wait_timeout for custom wait times')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
    state = module.params.get('state')
    try:
        if (state == 'present'):
            result = ensure_subnet_present(connection, module)
        elif (state == 'absent'):
            result = ensure_subnet_absent(connection, module)
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e)
    module.exit_json(**result)