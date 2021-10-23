def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), name=dict(required=True), description=dict(required=False), subnets=dict(required=False, type='list')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    state = module.params.get('state')
    group_name = module.params.get('name').lower()
    group_description = module.params.get('description')
    group_subnets = (module.params.get('subnets') or {
        
    })
    if (state == 'present'):
        for required in ['name', 'description', 'subnets']:
            if (not module.params.get(required)):
                module.fail_json(msg=str(("Parameter %s required for state='present'" % required)))
    else:
        for not_allowed in ['description', 'subnets']:
            if module.params.get(not_allowed):
                module.fail_json(msg=str(("Parameter %s not allowed for state='absent'" % not_allowed)))
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    if (not region):
        module.fail_json(msg=str('Either region or AWS_REGION or EC2_REGION environment variable or boto config aws_region or ec2_region must be set.'))
    'Get an elasticache connection'
    try:
        endpoint = ('elasticache.%s.amazonaws.com' % region)
        connect_region = RegionInfo(name=region, endpoint=endpoint)
        conn = ElastiCacheConnection(region=connect_region, **aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=e.message)
    try:
        changed = False
        exists = False
        try:
            matching_groups = conn.describe_cache_subnet_groups(group_name, max_records=100)
            exists = (len(matching_groups) > 0)
        except BotoServerError as e:
            if (e.error_code != 'CacheSubnetGroupNotFoundFault'):
                module.fail_json(msg=e.error_message)
        if (state == 'absent'):
            if exists:
                conn.delete_cache_subnet_group(group_name)
                changed = True
        elif (not exists):
            new_group = conn.create_cache_subnet_group(group_name, cache_subnet_group_description=group_description, subnet_ids=group_subnets)
            changed = True
        else:
            changed_group = conn.modify_cache_subnet_group(group_name, cache_subnet_group_description=group_description, subnet_ids=group_subnets)
            changed = True
    except BotoServerError as e:
        if (e.error_message != 'No modifications were requested.'):
            module.fail_json(msg=e.error_message)
        else:
            changed = False
    module.exit_json(changed=changed)