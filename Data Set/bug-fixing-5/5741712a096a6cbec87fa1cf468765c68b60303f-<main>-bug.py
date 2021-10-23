def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(filters=dict(default={
        
    }, type='dict')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if region:
        connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        module.fail_json(msg='region must be specified')
    sanitized_filters = module.params.get('filters')
    for key in sanitized_filters:
        if (not key.startswith('tag:')):
            sanitized_filters[key.replace('_', '-')] = sanitized_filters.pop(key)
    try:
        security_groups = connection.describe_security_groups(Filters=ansible_dict_to_boto3_filter_list(sanitized_filters))
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc())
    snaked_security_groups = []
    for security_group in security_groups['SecurityGroups']:
        security_group['Tags'] = boto3_tag_list_to_ansible_dict(security_group['Tags'])
        snaked_security_groups.append(camel_dict_to_snake_dict(security_group))
    module.exit_json(security_groups=snaked_security_groups)