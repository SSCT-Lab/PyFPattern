def ensure_subnet_present(conn, module, vpc_id, cidr, az, tags, map_public, check_mode):
    subnet = get_matching_subnet(conn, vpc_id, cidr)
    changed = False
    if (subnet is None):
        if (not check_mode):
            subnet = create_subnet(conn, module, vpc_id, cidr, az, check_mode)
        changed = True
        if (subnet is None):
            return {
                'changed': changed,
                'subnet': {
                    
                },
            }
    if (map_public != subnet['map_public_ip_on_launch']):
        ensure_map_public(conn, module, subnet, map_public, check_mode)
        subnet['map_public_ip_on_launch'] = map_public
        changed = True
    if (tags != subnet['tags']):
        ensure_tags(conn, module, subnet, tags, False, check_mode)
        subnet['tags'] = tags
        changed = True
    return {
        'changed': changed,
        'subnet': subnet,
    }