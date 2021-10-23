def ensure_subnet_associations(vpc_conn, vpc_id, route_table, subnets, check_mode, purge_subnets):
    current_association_ids = [a.id for a in route_table.associations if (not a.main)]
    new_association_ids = []
    changed = False
    for subnet in subnets:
        result = ensure_subnet_association(vpc_conn, vpc_id, route_table.id, subnet.id, check_mode)
        changed = (changed or result['changed'])
        if (changed and check_mode):
            return {
                'changed': True,
            }
        new_association_ids.append(result['association_id'])
    if purge_subnets:
        to_delete = [a_id for a_id in current_association_ids if (a_id not in new_association_ids)]
        for a_id in to_delete:
            changed = True
            vpc_conn.disassociate_route_table(a_id, dry_run=check_mode)
    return {
        'changed': changed,
    }