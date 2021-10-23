def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), name=dict(), link_aggregation_group_id=dict(), num_connections=dict(type='int'), min_links=dict(type='int'), location=dict(), bandwidth=dict(), connection_id=dict(), delete_with_disassociation=dict(type='bool', default=False), force_delete=dict(type='bool', default=False), wait=dict(type='bool', default=False), wait_timeout=dict(type='int', default=120)))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[('link_aggregation_group_id', 'name')], required_if=[('state', 'present', ('location', 'bandwidth'))])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    if (not region):
        module.fail_json(msg='Either region or AWS_REGION or EC2_REGION environment variable or boto config aws_region or ec2_region must be set.')
    connection = boto3_conn(module, conn_type='client', resource='directconnect', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    state = module.params.get('state')
    try:
        if (state == 'present'):
            (changed, lag_id) = ensure_present(connection, num_connections=module.params.get('num_connections'), lag_id=module.params.get('link_aggregation_group_id'), lag_name=module.params.get('name'), location=module.params.get('location'), bandwidth=module.params.get('bandwidth'), connection_id=module.params.get('connection_id'), min_links=module.params.get('min_links'), wait=module.params.get('wait'), wait_timeout=module.params.get('wait_timeout'))
            response = lag_status(connection, lag_id)
        elif (state == 'absent'):
            changed = ensure_absent(connection, lag_id=module.params.get('link_aggregation_group_id'), lag_name=module.params.get('name'), force_delete=module.params.get('force_delete'), delete_with_disassociation=module.params.get('delete_with_disassociation'), wait=module.params.get('wait'), wait_timeout=module.params.get('wait_timeout'))
            response = {
                
            }
    except DirectConnectError as e:
        if e.last_traceback:
            module.fail_json(msg=e.msg, exception=e.last_traceback, **camel_dict_to_snake_dict(e.exception.response))
        else:
            module.fail_json(msg=e.msg)
    module.exit_json(changed=changed, **camel_dict_to_snake_dict(response))