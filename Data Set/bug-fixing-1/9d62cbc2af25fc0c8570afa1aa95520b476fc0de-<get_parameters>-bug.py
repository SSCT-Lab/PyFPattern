

def get_parameters(client, module, parameters, method_name):
    required_options = get_boto3_client_method_parameters(client, method_name, required=True)
    if any([(parameters.get(k) is None) for k in required_options]):
        module.fail_json(msg='To {0} requires the parameters: {1}'.format(get_rds_method_attribute(method_name, module).operation_description, required_options))
    options = get_boto3_client_method_parameters(client, method_name)
    parameters = dict(((k, v) for (k, v) in parameters.items() if ((k in options) and (v is not None))))
    if (parameters.get('ProcessorFeatures') is not None):
        parameters['ProcessorFeatures'] = [{
            'Name': k,
            'Value': to_text(v),
        } for (k, v) in parameters['ProcessorFeatures'].items()]
    if ((parameters.get('ProcessorFeatures') == []) and (not (method_name == 'modify_db_instance'))):
        parameters.pop('ProcessorFeatures')
    if ((method_name == 'create_db_instance') and parameters.get('Tags')):
        parameters['Tags'] = ansible_dict_to_boto3_tag_list(parameters['Tags'])
    if (method_name == 'modify_db_instance'):
        parameters = get_options_with_changing_values(client, module, parameters)
    if (method_name == 'restore_db_instance_to_point_in_time'):
        parameters['TargetDBInstanceIdentifier'] = module.params['db_instance_identifier']
    return parameters
