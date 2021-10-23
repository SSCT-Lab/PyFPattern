def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), name=dict(), location=dict(), bandwidth=dict(choices=['1Gbps', '10Gbps']), link_aggregation_group=dict(), connection_id=dict(), forced_update=dict(type='bool', default=False)))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[('connection_id', 'name')], required_if=[('state', 'present', ('location', 'bandwidth'))])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    if (not region):
        module.fail_json(msg='Either region or AWS_REGION or EC2_REGION environment variable or boto config aws_region or ec2_region must be set.')
    connection = boto3_conn(module, conn_type='client', resource='directconnect', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    connection_id = connection_exists(connection, connection_id=module.params.get('connection_id'), connection_name=module.params.get('name'))
    if ((not connection_id) and module.params.get('connection_id')):
        module.fail_json(msg='The Direct Connect connection {0} does not exist.'.format(module.params.get('connection_id')))
    state = module.params.get('state')
    try:
        if (state == 'present'):
            (changed, connection_id) = ensure_present(connection, connection_id=connection_id, connection_name=module.params.get('name'), location=module.params.get('location'), bandwidth=module.params.get('bandwidth'), lag_id=module.params.get('link_aggregation_group'), forced_update=module.params.get('forced_update'))
            response = connection_status(connection, connection_id)
        elif (state == 'absent'):
            changed = ensure_absent(connection, connection_id)
            response = {
                
            }
    except DirectConnectError as e:
        if e.last_traceback:
            module.fail_json(msg=e.msg, exception=e.last_traceback, **camel_dict_to_snake_dict(e.exception.response))
        else:
            module.fail_json(msg=e.msg)
    module.exit_json(changed=changed, **camel_dict_to_snake_dict(response))