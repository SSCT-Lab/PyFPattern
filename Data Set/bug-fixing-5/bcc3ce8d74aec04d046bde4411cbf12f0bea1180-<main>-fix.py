def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(identity=dict(required=True, type='str'), state=dict(default='present', choices=['present', 'absent']), bounce_notifications=dict(type='dict'), complaint_notifications=dict(type='dict'), delivery_notifications=dict(type='dict'), feedback_forwarding=dict(default=True, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    for notification_type in ('bounce', 'complaint', 'delivery'):
        param_name = (notification_type + '_notifications')
        arg_dict = module.params.get(param_name)
        if arg_dict:
            extra_keys = [x for x in arg_dict.keys() if (x not in ('topic', 'include_headers'))]
            if extra_keys:
                module.fail_json(msg=(((('Unexpected keys ' + str(extra_keys)) + ' in ') + param_name) + ' valid keys are topic or include_headers'))
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    boto_core_config = Config(retries={
        'max_attempts': 9,
    })
    connection = boto3_conn(module, conn_type='client', resource='ses', region=region, endpoint=ec2_url, config=boto_core_config, **aws_connect_params)
    state = module.params.get('state')
    if (state == 'present'):
        sts = boto3_conn(module, conn_type='client', resource='sts', region=region, endpoint=ec2_url, **aws_connect_params)
        account_id = get_account_id(sts)
        create_or_update_identity(connection, module, region, account_id)
    else:
        destroy_identity(connection, module)