def ensure_routes(vpc_conn, route_table, route_specs, propagating_vgw_ids, check_mode, purge_routes):
    routes_to_match = list(route_table.routes)
    route_specs_to_create = []
    for route_spec in route_specs:
        i = index_of_matching_route(route_spec, routes_to_match)
        if (i is None):
            route_specs_to_create.append(route_spec)
        else:
            del routes_to_match[i]
    routes_to_delete = []
    if purge_routes:
        for r in routes_to_match:
            if r.gateway_id:
                if ((r.gateway_id != 'local') and (not r.gateway_id.startswith('vpce-'))):
                    if ((not propagating_vgw_ids) or (r.gateway_id not in propagating_vgw_ids)):
                        routes_to_delete.append(r)
            else:
                routes_to_delete.append(r)
    changed = bool((routes_to_delete or route_specs_to_create))
    if changed:
        for route in routes_to_delete:
            try:
                vpc_conn.delete_route(route_table.id, route.destination_cidr_block, dry_run=check_mode)
            except EC2ResponseError as e:
                if (e.error_code == 'DryRunOperation'):
                    pass
        for route_spec in route_specs_to_create:
            try:
                vpc_conn.create_route(route_table.id, dry_run=check_mode, **route_spec)
            except EC2ResponseError as e:
                if (e.error_code == 'DryRunOperation'):
                    pass
    return {
        'changed': bool(changed),
    }