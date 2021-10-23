def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), name=dict(), location=dict(), bandwidth=dict(choices=['1Gbps', '10Gbps']), link_aggregation_group=dict(), connection_id=dict(), forced_update=dict(type='bool', default=False)))
    module = AnsibleAWSModule(argument_spec=argument_spec, required_one_of=[('connection_id', 'name')], required_if=[('state', 'present', ('location', 'bandwidth'))])
    connection = module.client('directconnect')
    state = module.params.get('state')
    try:
        connection_id = connection_exists(connection, connection_id=module.params.get('connection_id'), connection_name=module.params.get('name'))
        if ((not connection_id) and module.params.get('connection_id')):
            module.fail_json(msg='The Direct Connect connection {0} does not exist.'.format(module.params.get('connection_id')))
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