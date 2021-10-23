def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(vpc_id=dict(required=True), state=dict(default='present', choices=['present', 'absent']), tags=dict(default=dict(), required=False, type='dict', aliases=['resource_tags'])))
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
    state = module.params.get('state', 'present')
    tags = module.params.get('tags')
    nonstring_tags = [k for (k, v) in tags.items() if (not isinstance(v, string_types))]
    if nonstring_tags:
        module.fail_json(msg='One or more tags contain non-string values: {0}'.format(nonstring_tags))
    try:
        if (state == 'present'):
            result = ensure_igw_present(connection, vpc_id, tags, check_mode=module.check_mode)
        elif (state == 'absent'):
            result = ensure_igw_absent(connection, vpc_id, check_mode=module.check_mode)
    except AnsibleIGWException as e:
        module.fail_json(msg=str(e))
    module.exit_json(**result)