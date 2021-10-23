def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(group_family=dict(type='str', choices=['memcached1.4', 'redis2.6', 'redis2.8', 'redis3.2']), name=dict(required=True, type='str'), description=dict(type='str'), state=dict(required=True), values=dict(type='dict')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto required for this module')
    parameter_group_family = module.params.get('group_family')
    parameter_group_name = module.params.get('name')
    group_description = module.params.get('description')
    state = module.params.get('state')
    values = module.params.get('values')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    if (not region):
        module.fail_json(msg='Either region or AWS_REGION or EC2_REGION environment variable or boto config aws_region or ec2_region must be set.')
    connection = boto3_conn(module, conn_type='client', resource='elasticache', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    exists = get_info(connection, parameter_group_name)
    if ((state == 'present') and (not (exists and parameter_group_family and group_description))):
        module.fail_json(msg='Creating a group requires a family group and a description.')
    elif ((state == 'reset') and (not exists)):
        module.fail_json(msg=("No group %s to reset. Please create the group before using the state 'reset'." % parameter_group_name))
    changed = False
    if (state == 'present'):
        if exists:
            if (not values):
                response = exists
                changed = False
            else:
                modifiable_params = make_current_modifiable_param_dict(module, connection, parameter_group_name)
                changed = check_valid_modification(module, values, modifiable_params)
                response = modify(module, connection, parameter_group_name, values)
        else:
            (response, changed) = create(module, connection, parameter_group_name, parameter_group_family, group_description)
            if values:
                modifiable_params = make_current_modifiable_param_dict(module, connection, parameter_group_name)
                changed = check_valid_modification(module, values, modifiable_params)
                response = modify(module, connection, parameter_group_name, values)
    elif (state == 'absent'):
        if exists:
            (response, changed) = delete(module, connection, parameter_group_name)
        else:
            response = {
                
            }
            changed = False
    elif (state == 'reset'):
        (response, changed) = reset(module, connection, parameter_group_name, values)
    facts_result = dict(changed=changed, elasticache=camel_dict_to_snake_dict(response))
    module.exit_json(**facts_result)