def _check_ips(module, cloud, server):
    changed = False
    auto_ip = module.params['auto_ip']
    floating_ips = module.params['floating_ips']
    floating_ip_pools = module.params['floating_ip_pools']
    if (floating_ip_pools or floating_ips):
        ips = openstack_find_nova_addresses(server.addresses, 'floating')
        if (not ips):
            server = cloud.add_ips_to_server(server, auto_ip=auto_ip, ips=floating_ips, ip_pool=floating_ip_pools, wait=module.params['wait'], timeout=module.params['timeout'])
            changed = True
        elif floating_ips:
            missing_ips = []
            for ip in floating_ips:
                if (ip not in ips):
                    missing_ips.append(ip)
            if missing_ips:
                server = cloud.add_ip_list(server, missing_ips, wait=module.params['wait'], timeout=module.params['timeout'])
                changed = True
            extra_ips = []
            for ip in ips:
                if (ip not in floating_ips):
                    extra_ips.append(ip)
            if extra_ips:
                _detach_ip_list(cloud, server, extra_ips)
                changed = True
    elif auto_ip:
        if server['interface_ip']:
            changed = False
        else:
            server = cloud.add_ips_to_server(server, auto_ip=auto_ip, ips=floating_ips, ip_pool=floating_ip_pools, wait=module.params['wait'], timeout=module.params['timeout'])
            changed = True
    return (changed, server)