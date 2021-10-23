def ensure_route_table_present(connection, module):
    lookup = module.params.get('lookup')
    propagating_vgw_ids = module.params.get('propagating_vgw_ids')
    purge_routes = module.params.get('purge_routes')
    purge_subnets = module.params.get('purge_subnets')
    purge_tags = module.params.get('purge_tags')
    route_table_id = module.params.get('route_table_id')
    subnets = module.params.get('subnets')
    tags = module.params.get('tags')
    vpc_id = module.params.get('vpc_id')
    routes = create_route_spec(connection, module, vpc_id)
    changed = False
    tags_valid = False
    if (lookup == 'tag'):
        if (tags is not None):
            try:
                route_table = get_route_table_by_tags(connection, module, vpc_id, tags)
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg="Error finding route table with lookup 'tag'")
        else:
            route_table = None
    elif (lookup == 'id'):
        try:
            route_table = get_route_table_by_id(connection, module, route_table_id)
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg="Error finding route table with lookup 'id'")
    if (route_table is None):
        changed = True
        if (not module.check_mode):
            try:
                route_table = connection.create_route_table(VpcId=vpc_id)['RouteTable']
                for attempt in range(5):
                    if (not get_route_table_by_id(connection, module, route_table['RouteTableId'])):
                        sleep(2)
                    else:
                        break
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg='Error creating route table')
        else:
            route_table = {
                'id': 'rtb-xxxxxxxx',
                'route_table_id': 'rtb-xxxxxxxx',
                'vpc_id': vpc_id,
            }
            module.exit_json(changed=changed, route_table=route_table)
    if (routes is not None):
        result = ensure_routes(connection=connection, module=module, route_table=route_table, route_specs=routes, propagating_vgw_ids=propagating_vgw_ids, check_mode=module.check_mode, purge_routes=purge_routes)
        changed = (changed or result['changed'])
    if (propagating_vgw_ids is not None):
        result = ensure_propagation(connection=connection, module=module, route_table=route_table, propagating_vgw_ids=propagating_vgw_ids, check_mode=module.check_mode)
        changed = (changed or result['changed'])
    if ((not tags_valid) and (tags is not None)):
        result = ensure_tags(connection=connection, module=module, resource_id=route_table['RouteTableId'], tags=tags, purge_tags=purge_tags, check_mode=module.check_mode)
        route_table['Tags'] = result['tags']
        changed = (changed or result['changed'])
    if (subnets is not None):
        associated_subnets = find_subnets(connection, module, vpc_id, subnets)
        result = ensure_subnet_associations(connection=connection, module=module, route_table=route_table, subnets=associated_subnets, check_mode=module.check_mode, purge_subnets=purge_subnets)
        changed = (changed or result['changed'])
    if changed:
        sleep(5)
    module.exit_json(changed=changed, route_table=get_route_table_info(connection, module, route_table))