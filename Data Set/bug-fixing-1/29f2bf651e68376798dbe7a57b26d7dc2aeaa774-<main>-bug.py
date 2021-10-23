

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(log_group_name=dict(required=True, type='str'), state=dict(choices=['present', 'absent'], default='present'), kms_key_id=dict(required=False, type='str'), tags=dict(required=False, type='dict'), retention=dict(required=False, type='int'), overwrite=dict(required=False, type='bool', default=False)))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required.')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    logs = boto3_conn(module, conn_type='client', resource='logs', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    state = module.params.get('state')
    changed = False
    desc_log_group = describe_log_group(client=logs, log_group_name=module.params['log_group_name'], module=module)
    found_log_group = {
        
    }
    for i in desc_log_group.get('logGroups', []):
        if (module.params['log_group_name'] == i['logGroupName']):
            found_log_group = i
            break
    if (state == 'present'):
        if (found_log_group and (module.params['overwrite'] is True)):
            changed = True
            delete_log_group(client=logs, log_group_name=module.params['log_group_name'], module=module)
            found_log_group = create_log_group(client=logs, log_group_name=module.params['log_group_name'], kms_key_id=module.params['kms_key_id'], tags=module.params['tags'], retention=module.params['retention'], module=module)
        elif (not found_log_group):
            changed = True
            found_log_group = create_log_group(client=logs, log_group_name=module.params['log_group_name'], kms_key_id=module.params['kms_key_id'], tags=module.params['tags'], retention=module.params['retention'], module=module)
        module.exit_json(changed=changed, **camel_dict_to_snake_dict(found_log_group))
    elif (state == 'absent'):
        if found_log_group:
            changed = True
            delete_log_group(client=logs, log_group_name=module.params['log_group_name'], module=module)
    module.exit_json(changed=changed)
