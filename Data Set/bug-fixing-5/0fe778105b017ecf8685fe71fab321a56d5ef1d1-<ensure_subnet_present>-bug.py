def ensure_subnet_present(conn, module):
    subnet = get_matching_subnet(conn, module, module.params['vpc_id'], module.params['cidr'])
    changed = False
    start_time = time.time()
    if (subnet is None):
        if (not module.check_mode):
            subnet = create_subnet(conn, module, module.params['vpc_id'], module.params['cidr'], ipv6_cidr=module.params['ipv6_cidr'], az=module.params['az'], start_time=start_time)
        changed = True
        if (subnet is None):
            return {
                'changed': changed,
                'subnet': {
                    
                },
            }
    if module.params['wait']:
        handle_waiter(conn, module, 'subnet_exists', {
            'SubnetIds': [subnet['id']],
        }, start_time)
    if (module.params['ipv6_cidr'] != subnet.get('ipv6_cidr_block')):
        if ensure_ipv6_cidr_block(conn, module, subnet, module.params['ipv6_cidr'], module.check_mode, start_time):
            changed = True
    if (module.params['map_public'] != subnet['map_public_ip_on_launch']):
        ensure_map_public(conn, module, subnet, module.params['map_public'], module.check_mode, start_time)
        changed = True
    if (module.params['assign_instances_ipv6'] != subnet.get('assign_ipv6_address_on_creation')):
        ensure_assign_ipv6_on_create(conn, module, subnet, module.params['assign_instances_ipv6'], module.check_mode, start_time)
        changed = True
    if (module.params['tags'] != subnet['tags']):
        stringified_tags_dict = dict(((to_text(k), to_text(v)) for (k, v) in module.params['tags'].items()))
        if ensure_tags(conn, module, subnet, stringified_tags_dict, module.params['purge_tags'], start_time):
            changed = True
    subnet = get_matching_subnet(conn, module, module.params['vpc_id'], module.params['cidr'])
    return {
        'changed': changed,
        'subnet': subnet,
    }