

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(az=dict(default=None, required=False), cidr=dict(default=None, required=True), state=dict(default='present', choices=['present', 'absent']), tags=dict(default=None, required=False, type='dict', aliases=['resource_tags']), vpc_id=dict(default=None, required=True)))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto is required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if region:
        try:
            connection = connect_to_aws(boto.vpc, region, **aws_connect_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))
    else:
        module.fail_json(msg='region must be specified')
    vpc_id = module.params.get('vpc_id')
    tags = module.params.get('tags')
    cidr = module.params.get('cidr')
    az = module.params.get('az')
    state = module.params.get('state')
    try:
        if (state == 'present'):
            result = ensure_subnet_present(connection, vpc_id, cidr, az, tags, check_mode=module.check_mode)
        elif (state == 'absent'):
            result = ensure_subnet_absent(connection, vpc_id, cidr, check_mode=module.check_mode)
    except AnsibleVPCSubnetException as e:
        module.fail_json(msg=str(e))
    module.exit_json(**result)
