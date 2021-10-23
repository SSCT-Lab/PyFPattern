def validate_parameters(required_vars, valid_vars, module):
    command = module.params.get('command')
    for v in required_vars:
        if (not module.params.get(v)):
            module.fail_json(msg=('Parameter %s required for %s command' % (v, command)))
    optional_params = {
        'port': 'port',
        'db_name': 'db_name',
        'zone': 'availability_zone',
        'maint_window': 'preferred_maintenance_window',
        'backup_window': 'preferred_backup_window',
        'backup_retention': 'backup_retention_period',
        'multi_zone': 'multi_az',
        'engine_version': 'engine_version',
        'upgrade': 'auto_minor_version_upgrade',
        'subnet': 'db_subnet_group_name',
        'license_model': 'license_model',
        'option_group': 'option_group_name',
        'size': 'allocated_storage',
        'iops': 'iops',
        'new_instance_name': 'new_instance_id',
        'apply_immediately': 'apply_immediately',
    }
    optional_params_rds = {
        'db_engine': 'engine',
        'password': 'master_password',
        'parameter_group': 'param_group',
        'instance_type': 'instance_class',
    }
    optional_params_rds2 = {
        'tags': 'tags',
        'publicly_accessible': 'publicly_accessible',
        'parameter_group': 'db_parameter_group_name',
        'character_set_name': 'character_set_name',
        'instance_type': 'db_instance_class',
        'password': 'master_user_password',
        'new_instance_name': 'new_db_instance_identifier',
        'force_failover': 'force_failover',
    }
    if has_rds2:
        optional_params.update(optional_params_rds2)
        sec_group = 'db_security_groups'
    else:
        optional_params.update(optional_params_rds)
        sec_group = 'security_groups'
        for k in (set(optional_params_rds2.keys()) - set(optional_params_rds.keys())):
            if module.params.get(k):
                module.fail_json(msg=('Parameter %s requires boto.rds (boto >= 2.26.0)' % k))
    params = {
        
    }
    for (k, v) in optional_params.items():
        if ((module.params.get(k) is not None) and (k not in required_vars)):
            if (k in valid_vars):
                params[v] = module.params[k]
            elif (module.params.get(k) == False):
                pass
            else:
                module.fail_json(msg=('Parameter %s is not valid for %s command' % (k, command)))
    if module.params.get('security_groups'):
        params[sec_group] = module.params.get('security_groups').split(',')
    vpc_groups = module.params.get('vpc_security_groups')
    if vpc_groups:
        if has_rds2:
            params['vpc_security_group_ids'] = vpc_groups
        else:
            groups_list = []
            for x in vpc_groups:
                groups_list.append(boto.rds.VPCSecurityGroupMembership(vpc_group=x))
            params['vpc_security_groups'] = groups_list
    if ('tags' in params):
        params['tags'] = module.params['tags'].items()
    return params