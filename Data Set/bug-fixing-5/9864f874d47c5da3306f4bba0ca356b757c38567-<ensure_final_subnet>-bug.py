def ensure_final_subnet(conn, module, subnet, start_time):
    for rewait in range(0, 10):
        map_public_correct = False
        assign_ipv6_correct = False
        if (module.params['map_public'] == subnet['map_public_ip_on_launch']):
            map_public_correct = True
        elif module.params['map_public']:
            handle_waiter(conn, module, 'subnet_has_map_public', {
                'SubnetIds': [subnet['id']],
            }, start_time)
        else:
            handle_waiter(conn, module, 'subnet_no_map_public', {
                'SubnetIds': [subnet['id']],
            }, start_time)
        if (module.params['assign_instances_ipv6'] == subnet.get('assign_ipv6_address_on_creation')):
            assign_ipv6_correct = True
        elif module.params['assign_instances_ipv6']:
            handle_waiter(conn, module, 'subnet_has_assign_ipv6', {
                'SubnetIds': [subnet['id']],
            }, start_time)
        else:
            handle_waiter(conn, module, 'subnet_no_assign_ipv6', {
                'SubnetIds': [subnet['id']],
            }, start_time)
        if (map_public_correct and assign_ipv6_correct):
            break
        time.sleep(3)
        subnet = get_matching_subnet(conn, module, module.params['vpc_id'], module.params['cidr'])
    return subnet