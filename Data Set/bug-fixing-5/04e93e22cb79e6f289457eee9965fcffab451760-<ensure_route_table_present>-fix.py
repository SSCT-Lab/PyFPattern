def ensure_route_table_present(connection, module):
    lookup = module.params.get('lookup')
    propagating_vgw_ids = module.params.get('propagating_vgw_ids')
    purge_routes = module.params.get('purge_routes')
    purge_subnets = module.params.get('purge_subnets')
    route_table_id = module.params.get('route_table_id')
    subnets = module.params.get('subnets')
    tags = module.params.get('tags')
    vpc_id = module.params.get('vpc_id')
    try:
        routes = create_route_spec(connection, module, vpc_id)
    except AnsibleIgwSearchException as e:
        module.fail_json(msg='Failed to find the Internet gateway for the given VPC ID {0}: {1}'.format(vpc_id, e[0]), exception=traceback.format_exc())
    changed = False
    tags_valid = False
    if (lookup == 'tag'):
        if (tags is not None):
            try:
                route_table = get_route_table_by_tags(connection, vpc_id, tags)
            except EC2ResponseError as e:
                module.fail_json(msg="Error finding route table with lookup 'tag': {0}".format(e.message), exception=traceback.format_exc())
            except RuntimeError as e:
                module.fail_json(msg=e.args[0], exception=traceback.format_exc())
        else:
            route_table = None
    elif (lookup == 'id'):
        try:
            route_table = get_route_table_by_id(connection, vpc_id, route_table_id)
        except EC2ResponseError as e:
            module.fail_json(msg="Error finding route table with lookup 'id': {0}".format(e.message), exception=traceback.format_exc())
    if (route_table is None):
        try:
            route_table = connection.create_route_table(vpc_id, module.check_mode)
            changed = True
        except EC2ResponseError as e:
            if (e.error_code == 'DryRunOperation'):
                module.exit_json(changed=True)
            module.fail_json(msg='Failed to create route table: {0}'.format(e.message), exception=traceback.format_exc())
    if (routes is not None):
        try:
            result = ensure_routes(connection, route_table, routes, propagating_vgw_ids, module.check_mode, purge_routes)
            changed = (changed or result['changed'])
        except EC2ResponseError as e:
            module.fail_json(msg='Error while updating routes: {0}'.format(e.message), exception=traceback.format_exc())
    if (propagating_vgw_ids is not None):
        result = ensure_propagation(connection, route_table, propagating_vgw_ids, check_mode=module.check_mode)
        changed = (changed or result['changed'])
    if ((not tags_valid) and (tags is not None)):
        result = ensure_tags(connection, route_table.id, tags, add_only=True, check_mode=module.check_mode)
        route_table.tags = result['tags']
        changed = (changed or result['changed'])
    if subnets:
        associated_subnets = []
        try:
            associated_subnets = find_subnets(connection, vpc_id, subnets)
        except EC2ResponseError as e:
            raise AnsibleRouteTableException(message='Unable to find subnets for route table {0}, error: {1}'.format(route_table, e), error_traceback=traceback.format_exc())
        try:
            result = ensure_subnet_associations(connection, vpc_id, route_table, associated_subnets, module.check_mode, purge_subnets)
            changed = (changed or result['changed'])
        except EC2ResponseError as e:
            raise AnsibleRouteTableException(message='Unable to associate subnets for route table {0}, error: {1}'.format(route_table, e), error_traceback=traceback.format_exc())
    module.exit_json(changed=changed, route_table=get_route_table_info(route_table))