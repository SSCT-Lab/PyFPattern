

def main():
    arg_spec = dict(state=dict(choices=['present', 'absent', 'terminated', 'running', 'started', 'stopped', 'rebooted', 'restarted'], default='present'), creation_source=dict(choices=['snapshot', 's3', 'instance']), force_update_password=dict(type='bool', default=False), purge_cloudwatch_logs_exports=dict(type='bool', default=True), purge_tags=dict(type='bool', default=True), read_replica=dict(type='bool'), wait=dict(type='bool', default=True))
    parameter_options = dict(allocated_storage=dict(type='int'), allow_major_version_upgrade=dict(type='bool'), apply_immediately=dict(type='bool', default=False), auto_minor_version_upgrade=dict(type='bool'), availability_zone=dict(aliases=['az', 'zone']), backup_retention_period=dict(type='int'), ca_certificate_identifier=dict(), character_set_name=dict(), copy_tags_to_snapshot=dict(type='bool'), db_cluster_identifier=dict(aliases=['cluster_id']), db_instance_class=dict(aliases=['class', 'instance_type']), db_instance_identifier=dict(required=True, aliases=['instance_id', 'id']), db_name=dict(), db_parameter_group_name=dict(), db_security_groups=dict(type='list'), db_snapshot_identifier=dict(), db_subnet_group_name=dict(aliases=['subnet_group']), domain=dict(), domain_iam_role_name=dict(), enable_cloudwatch_logs_exports=dict(type='list', aliases=['cloudwatch_log_exports']), enable_iam_database_authentication=dict(type='bool'), enable_performance_insights=dict(type='bool'), engine=dict(), engine_version=dict(), final_db_snapshot_identifier=dict(aliases=['final_snapshot_identifier']), force_failover=dict(type='bool'), iops=dict(type='int'), kms_key_id=dict(), license_model=dict(choices=['license-included', 'bring-your-own-license', 'general-public-license']), master_user_password=dict(aliases=['password'], no_log=True), master_username=dict(aliases=['username']), monitoring_interval=dict(type='int'), monitoring_role_arn=dict(), multi_az=dict(type='bool'), new_db_instance_identifier=dict(aliases=['new_instance_id', 'new_id']), option_group_name=dict(), performance_insights_kms_key_id=dict(), performance_insights_retention_period=dict(), port=dict(type='int'), preferred_backup_window=dict(aliases=['backup_window']), preferred_maintenance_window=dict(aliases=['maintenance_window']), processor_features=dict(type='dict'), promotion_tier=dict(), publicly_accessible=dict(type='bool'), restore_time=dict(), s3_bucket_name=dict(), s3_ingestion_role_arn=dict(), s3_prefix=dict(), skip_final_snapshot=dict(type='bool', default=False), snapshot_identifier=dict(), source_db_instance_identifier=dict(), source_engine=dict(choices=['mysql']), source_engine_version=dict(), source_region=dict(), storage_encrypted=dict(type='bool'), storage_type=dict(choices=['standard', 'gp2', 'io1']), tags=dict(type='dict'), tde_credential_arn=dict(aliases=['transparent_data_encryption_arn']), tde_credential_password=dict(no_log=True, aliases=['transparent_data_encryption_password']), timezone=dict(), use_latest_restorable_time=dict(type='bool', aliases=['restore_from_latest']), vpc_security_group_ids=dict(type='list'))
    arg_spec.update(parameter_options)
    required_if = [('engine', 'aurora', ('db_cluster_identifier',)), ('engine', 'aurora-mysql', ('db_cluster_identifier',)), ('engine', 'aurora-postresql', ('db_cluster_identifier',)), ('creation_source', 'snapshot', ('snapshot_identifier', 'engine')), ('creation_source', 's3', ('s3_bucket_name', 'engine', 'master_username', 'master_user_password', 'source_engine', 'source_engine_version', 's3_ingestion_role_arn'))]
    mutually_exclusive = [('s3_bucket_name', 'source_db_instance_identifier', 'snapshot_identifier'), ('use_latest_restorable_time', 'restore_to_time'), ('availability_zone', 'multi_az')]
    module = AnsibleAWSModule(argument_spec=arg_spec, required_if=required_if, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    if (not module.boto3_at_least('1.5.0')):
        module.fail_json(msg='rds_instance requires boto3 > 1.5.0')
    module.params['db_instance_identifier'] = module.params['db_instance_identifier'].lower()
    if module.params['new_db_instance_identifier']:
        module.params['new_db_instance_identifier'] = module.params['new_db_instance_identifier'].lower()
    if (module.params['processor_features'] is not None):
        module.params['processor_features'] = dict(((k, to_text(v)) for (k, v) in module.params['processor_features'].items()))
    client = module.client('rds')
    changed = False
    state = module.params['state']
    instance_id = module.params['db_instance_identifier']
    instance = get_instance(client, module, instance_id)
    validate_options(client, module, instance)
    method_name = get_rds_method_attribute_name(instance, state, module.params['creation_source'], module.params['read_replica'])
    if method_name:
        raw_parameters = arg_spec_to_rds_params(dict(((k, module.params[k]) for k in module.params if (k in parameter_options))))
        parameters = get_parameters(client, module, raw_parameters, method_name)
        if parameters:
            (result, changed) = call_method(client, module, method_name, parameters)
        instance_id = get_final_identifier(method_name, module)
        if ((state != 'absent') and ((not module.check_mode) or instance)):
            changed |= update_instance(client, module, instance, instance_id)
        if changed:
            instance = get_instance(client, module, instance_id)
            if ((state != 'absent') and (instance or (not module.check_mode))):
                for attempt_to_wait in range(0, 10):
                    instance = get_instance(client, module, instance_id)
                    if instance:
                        break
                    else:
                        sleep(5)
        if ((state == 'absent') and changed and (not module.params['skip_final_snapshot'])):
            instance.update(FinalSnapshot=get_final_snapshot(client, module, module.params['final_db_snapshot_identifier']))
    pending_processor_features = None
    if instance.get('PendingModifiedValues', {
        
    }).get('ProcessorFeatures'):
        pending_processor_features = instance['PendingModifiedValues'].pop('ProcessorFeatures')
    instance = camel_dict_to_snake_dict(instance, ignore_list=['Tags', 'ProcessorFeatures'])
    if (pending_processor_features is not None):
        instance['pending_modified_values']['processor_features'] = pending_processor_features
    module.exit_json(changed=changed, **instance)
