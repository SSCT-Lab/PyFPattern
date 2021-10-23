def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state={
        'required': True,
        'choices': ['present', 'absent'],
    }, name={
        'required': True,
    }, listeners={
        'default': None,
        'required': False,
        'type': 'list',
    }, purge_listeners={
        'default': True,
        'required': False,
        'type': 'bool',
    }, instance_ids={
        'default': None,
        'required': False,
        'type': 'list',
    }, purge_instance_ids={
        'default': False,
        'required': False,
        'type': 'bool',
    }, zones={
        'default': None,
        'required': False,
        'type': 'list',
    }, purge_zones={
        'default': False,
        'required': False,
        'type': 'bool',
    }, security_group_ids={
        'default': None,
        'required': False,
        'type': 'list',
    }, security_group_names={
        'default': None,
        'required': False,
        'type': 'list',
    }, health_check={
        'default': None,
        'required': False,
        'type': 'dict',
    }, subnets={
        'default': None,
        'required': False,
        'type': 'list',
    }, purge_subnets={
        'default': False,
        'required': False,
        'type': 'bool',
    }, scheme={
        'default': 'internet-facing',
        'required': False,
    }, connection_draining_timeout={
        'default': None,
        'required': False,
    }, idle_timeout={
        'default': None,
        'required': False,
    }, cross_az_load_balancing={
        'default': None,
        'required': False,
    }, stickiness={
        'default': None,
        'required': False,
        'type': 'dict',
    }, access_logs={
        'default': None,
        'required': False,
        'type': 'dict',
    }, wait={
        'default': False,
        'type': 'bool',
        'required': False,
    }, wait_timeout={
        'default': 60,
        'type': 'int',
        'required': False,
    }, tags={
        'default': None,
        'required': False,
        'type': 'dict',
    }))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['security_group_ids', 'security_group_names']])
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if (not region):
        module.fail_json(msg='Region must be specified as a parameter, in EC2_REGION or AWS_REGION environment variables or in boto configuration file')
    name = module.params['name']
    state = module.params['state']
    listeners = module.params['listeners']
    purge_listeners = module.params['purge_listeners']
    instance_ids = module.params['instance_ids']
    purge_instance_ids = module.params['purge_instance_ids']
    zones = module.params['zones']
    purge_zones = module.params['purge_zones']
    security_group_ids = module.params['security_group_ids']
    security_group_names = module.params['security_group_names']
    health_check = module.params['health_check']
    access_logs = module.params['access_logs']
    subnets = module.params['subnets']
    purge_subnets = module.params['purge_subnets']
    scheme = module.params['scheme']
    connection_draining_timeout = module.params['connection_draining_timeout']
    idle_timeout = module.params['idle_timeout']
    cross_az_load_balancing = module.params['cross_az_load_balancing']
    stickiness = module.params['stickiness']
    wait = module.params['wait']
    wait_timeout = module.params['wait_timeout']
    tags = module.params['tags']
    if ((state == 'present') and (not listeners)):
        module.fail_json(msg='At least one listener is required for ELB creation')
    if ((state == 'present') and (not (zones or subnets))):
        module.fail_json(msg='At least one availability zone or subnet is required for ELB creation')
    if (wait_timeout > 600):
        module.fail_json(msg='wait_timeout maximum is 600 seconds')
    if security_group_names:
        security_group_ids = []
        try:
            ec2 = ec2_connect(module)
            if subnets:
                vpc_conn = _get_vpc_connection(module=module, region=region, aws_connect_params=aws_connect_params)
                vpc_id = vpc_conn.get_all_subnets([subnets[0]])[0].vpc_id
                filters = {
                    'vpc_id': vpc_id,
                }
            else:
                filters = None
            grp_details = ec2.get_all_security_groups(filters=filters)
            for group_name in security_group_names:
                if isinstance(group_name, basestring):
                    group_name = [group_name]
                group_id = [str(grp.id) for grp in grp_details if (str(grp.name) in group_name)]
                security_group_ids.extend(group_id)
        except boto.exception.NoAuthHandlerFound as e:
            module.fail_json(msg=str(e))
    elb_man = ElbManager(module, name, listeners, purge_listeners, zones, purge_zones, security_group_ids, health_check, subnets, purge_subnets, scheme, connection_draining_timeout, idle_timeout, cross_az_load_balancing, access_logs, stickiness, wait, wait_timeout, tags, region=region, instance_ids=instance_ids, purge_instance_ids=purge_instance_ids, **aws_connect_params)
    if (cross_az_load_balancing and (not elb_man._check_attribute_support('cross_zone_load_balancing'))):
        module.fail_json(msg='You must install boto >= 2.18.0 to use the cross_az_load_balancing attribute')
    if (connection_draining_timeout and (not elb_man._check_attribute_support('connection_draining'))):
        module.fail_json(msg='You must install boto >= 2.28.0 to use the connection_draining_timeout attribute')
    if (idle_timeout and (not elb_man._check_attribute_support('connecting_settings'))):
        module.fail_json(msg='You must install boto >= 2.33.0 to use the idle_timeout attribute')
    if (state == 'present'):
        elb_man.ensure_ok()
    elif (state == 'absent'):
        elb_man.ensure_gone()
    ansible_facts = {
        'ec2_elb': 'info',
    }
    ec2_facts_result = dict(changed=elb_man.changed, elb=elb_man.get_info(), ansible_facts=ansible_facts)
    module.exit_json(**ec2_facts_result)