

def ensure_route_table_absent(connection, module):
    lookup = module.params.get('lookup')
    route_table_id = module.params.get('route_table_id')
    tags = module.params.get('tags')
    vpc_id = module.params.get('vpc_id')
    if (lookup == 'tag'):
        if (tags is not None):
            try:
                route_table = get_route_table_by_tags(connection, vpc_id, tags)
            except EC2ResponseError as e:
                module.fail_json(msg=e.message)
            except RuntimeError as e:
                module.fail_json(msg=e.args[0])
        else:
            route_table = None
    elif (lookup == 'id'):
        try:
            route_table = get_route_table_by_id(connection, vpc_id, route_table_id)
        except EC2ResponseError as e:
            module.fail_json(msg=e.message)
    if (route_table is None):
        return {
            'changed': False,
        }
    try:
        connection.delete_route_table(route_table.id, dry_run=module.check_mode)
    except EC2ResponseError as e:
        if (e.error_code == 'DryRunOperation'):
            pass
        else:
            module.fail_json(msg=e.message)
    return {
        'changed': True,
    }
