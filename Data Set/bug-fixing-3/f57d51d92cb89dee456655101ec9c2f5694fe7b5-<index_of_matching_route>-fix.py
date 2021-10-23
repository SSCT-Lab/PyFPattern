def index_of_matching_route(route_spec, routes_to_match):
    for (i, route) in enumerate(routes_to_match):
        if route_spec_matches_route(route_spec, route):
            return i
        elif route_spec_matches_route_cidr(route_spec, route):
            return 'replace'