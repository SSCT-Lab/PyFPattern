def main():
    ' elasticache ansible module '
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state={
        'required': True,
        'choices': ['present', 'absent', 'rebooted'],
    }, name={
        'required': True,
    }, engine={
        'required': False,
        'default': 'memcached',
    }, cache_engine_version={
        'required': False,
        'default': '',
    }, node_type={
        'required': False,
        'default': 'cache.t2.small',
    }, num_nodes={
        'required': False,
        'default': 1,
        'type': 'int',
    }, cache_parameter_group={
        'required': False,
        'default': '',
        'aliases': ['parameter_group'],
    }, cache_port={
        'required': False,
        'type': 'int',
        'default': None,
    }, cache_subnet_group={
        'required': False,
        'default': '',
    }, cache_security_groups={
        'required': False,
        'default': [],
        'type': 'list',
    }, security_group_ids={
        'required': False,
        'default': [],
        'type': 'list',
    }, zone={
        'required': False,
        'default': '',
    }, wait={
        'required': False,
        'default': True,
        'type': 'bool',
    }, hard_modify={
        'required': False,
        'default': False,
        'type': 'bool',
    }))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    name = module.params['name']
    state = module.params['state']
    engine = module.params['engine']
    cache_engine_version = module.params['cache_engine_version']
    node_type = module.params['node_type']
    num_nodes = module.params['num_nodes']
    cache_port = module.params['cache_port']
    cache_subnet_group = module.params['cache_subnet_group']
    cache_security_groups = module.params['cache_security_groups']
    security_group_ids = module.params['security_group_ids']
    zone = module.params['zone']
    wait = module.params['wait']
    hard_modify = module.params['hard_modify']
    cache_parameter_group = module.params['cache_parameter_group']
    if (cache_subnet_group and cache_security_groups):
        module.fail_json(msg="Can't specify both cache_subnet_group and cache_security_groups")
    if ((state == 'present') and (not num_nodes)):
        module.fail_json(msg="'num_nodes' is a required parameter. Please specify num_nodes > 0")
    elasticache_manager = ElastiCacheManager(module, name, engine, cache_engine_version, node_type, num_nodes, cache_port, cache_parameter_group, cache_subnet_group, cache_security_groups, security_group_ids, zone, wait, hard_modify, region, **aws_connect_kwargs)
    if (state == 'present'):
        elasticache_manager.ensure_present()
    elif (state == 'absent'):
        elasticache_manager.ensure_absent()
    elif (state == 'rebooted'):
        elasticache_manager.ensure_rebooted()
    facts_result = dict(changed=elasticache_manager.changed, elasticache=elasticache_manager.get_info())
    module.exit_json(**facts_result)