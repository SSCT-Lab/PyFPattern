def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(lookup=dict(default='tag', required=False, choices=['tag', 'id']), propagating_vgw_ids=dict(default=None, required=False, type='list'), purge_routes=dict(default=True, type='bool'), purge_subnets=dict(default=True, type='bool'), route_table_id=dict(default=None, required=False), routes=dict(default=[], required=False, type='list'), state=dict(default='present', choices=['present', 'absent']), subnets=dict(default=None, required=False, type='list'), tags=dict(default=None, required=False, type='dict', aliases=['resource_tags']), vpc_id=dict(default=None, required=True)))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto is required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if region:
        try:
            connection = connect_to_aws(boto.vpc, region, **aws_connect_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))
    else:
        module.fail_json(msg='region must be specified')
    lookup = module.params.get('lookup')
    route_table_id = module.params.get('route_table_id')
    state = module.params.get('state', 'present')
    if ((lookup == 'id') and (route_table_id is None)):
        module.fail_json(msg='You must specify route_table_id if lookup is set to id')
    try:
        if (state == 'present'):
            result = ensure_route_table_present(connection, module)
        elif (state == 'absent'):
            result = ensure_route_table_absent(connection, module)
    except AnsibleRouteTableException as e:
        if e.error_traceback:
            module.fail_json(msg=e.message, exception=e.error_traceback)
        module.fail_json(msg=e.message)
    module.exit_json(**result)