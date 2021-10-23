def ensure_subnet_association(vpc_conn, vpc_id, route_table_id, subnet_id, check_mode):
    route_tables = vpc_conn.get_all_route_tables(filters={
        'association.subnet_id': subnet_id,
        'vpc_id': vpc_id,
    })
    for route_table in route_tables:
        if (route_table.id is None):
            continue
        for a in route_table.associations:
            if (a.subnet_id == subnet_id):
                if (route_table.id == route_table_id):
                    return {
                        'changed': False,
                        'association_id': a.id,
                    }
                else:
                    if check_mode:
                        return {
                            'changed': True,
                        }
                    vpc_conn.disassociate_route_table(a.id)
    association_id = vpc_conn.associate_route_table(route_table_id, subnet_id)
    return {
        'changed': True,
        'association_id': association_id,
    }