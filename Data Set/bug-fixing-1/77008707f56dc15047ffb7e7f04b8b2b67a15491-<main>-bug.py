

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(command=dict(choices=['create', 'replicate', 'delete', 'facts', 'modify', 'promote', 'snapshot', 'reboot', 'restore'], required=True), instance_name=dict(required=False), source_instance=dict(required=False), db_engine=dict(choices=['mariadb', 'MySQL', 'oracle-se1', 'oracle-se', 'oracle-ee', 'sqlserver-ee', 'sqlserver-se', 'sqlserver-ex', 'sqlserver-web', 'postgres', 'aurora'], required=False), size=dict(required=False), instance_type=dict(aliases=['type'], required=False), username=dict(required=False), password=dict(no_log=True, required=False), db_name=dict(required=False), engine_version=dict(required=False), parameter_group=dict(required=False), license_model=dict(choices=['license-included', 'bring-your-own-license', 'general-public-license', 'postgresql-license'], required=False), multi_zone=dict(type='bool', required=False), iops=dict(required=False), security_groups=dict(required=False), vpc_security_groups=dict(type='list', required=False), port=dict(required=False), upgrade=dict(type='bool', default=False), option_group=dict(required=False), maint_window=dict(required=False), backup_window=dict(required=False), backup_retention=dict(required=False), zone=dict(aliases=['aws_zone', 'ec2_zone'], required=False), subnet=dict(required=False), wait=dict(type='bool', default=False), wait_timeout=dict(type='int', default=300), snapshot=dict(required=False), apply_immediately=dict(type='bool', default=False), new_instance_name=dict(required=False), tags=dict(type='dict', required=False), publicly_accessible=dict(required=False), character_set_name=dict(required=False), force_failover=dict(type='bool', required=False, default=False)))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    invocations = {
        'create': create_db_instance,
        'replicate': replicate_db_instance,
        'delete': delete_db_instance_or_snapshot,
        'facts': facts_db_instance_or_snapshot,
        'modify': modify_db_instance,
        'promote': promote_db_instance,
        'snapshot': snapshot_db_instance,
        'reboot': reboot_db_instance,
        'restore': restore_db_instance,
    }
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if (not region):
        module.fail_json(msg='Region not specified. Unable to determine region from EC2_REGION.')
    if ((module.params['port'] is None) and (module.params['db_engine'] is not None) and (module.params['command'] == 'create')):
        if ('-' in module.params['db_engine']):
            engine = module.params['db_engine'].split('-')[0]
        else:
            engine = module.params['db_engine']
        module.params['port'] = DEFAULT_PORTS[engine.lower()]
    if has_rds2:
        conn = RDS2Connection(module, region, **aws_connect_params)
    else:
        conn = RDSConnection(module, region, **aws_connect_params)
    invocations[module.params.get('command')](module, conn)
