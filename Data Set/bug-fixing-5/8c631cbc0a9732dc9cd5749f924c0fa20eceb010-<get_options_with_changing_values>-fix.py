def get_options_with_changing_values(client, module, parameters):
    instance_id = module.params['db_instance_identifier']
    purge_cloudwatch_logs = module.params['purge_cloudwatch_logs_exports']
    force_update_password = module.params['force_update_password']
    port = module.params['port']
    apply_immediately = parameters.pop('ApplyImmediately', None)
    cloudwatch_logs_enabled = module.params['enable_cloudwatch_logs_exports']
    if port:
        parameters['DBPortNumber'] = port
    if (not force_update_password):
        parameters.pop('MasterUserPassword', None)
    if cloudwatch_logs_enabled:
        parameters['CloudwatchLogsExportConfiguration'] = cloudwatch_logs_enabled
    if (not module.params['storage_type']):
        parameters.pop('Iops')
    instance = get_instance(client, module, instance_id)
    updated_parameters = get_changing_options_with_inconsistent_keys(parameters, instance, purge_cloudwatch_logs)
    updated_parameters.update(get_changing_options_with_consistent_keys(parameters, instance))
    parameters = updated_parameters
    if (parameters.get('NewDBInstanceIdentifier') and instance.get('PendingModifiedValues', {
        
    }).get('DBInstanceIdentifier')):
        if ((parameters['NewDBInstanceIdentifier'] == instance['PendingModifiedValues']['DBInstanceIdentifier']) and (not apply_immediately)):
            parameters.pop('NewDBInstanceIdentifier')
    if parameters:
        parameters['DBInstanceIdentifier'] = instance_id
        if (apply_immediately is not None):
            parameters['ApplyImmediately'] = apply_immediately
    return parameters