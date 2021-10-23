def _needs_update(subnet, module, cloud, filters=None):
    'Check for differences in the updatable values.'
    _can_update(subnet, module, cloud, filters)
    enable_dhcp = module.params['enable_dhcp']
    subnet_name = module.params['name']
    pool_start = module.params['allocation_pool_start']
    pool_end = module.params['allocation_pool_end']
    gateway_ip = module.params['gateway_ip']
    no_gateway_ip = module.params['no_gateway_ip']
    dns = module.params['dns_nameservers']
    host_routes = module.params['host_routes']
    curr_pool = subnet['allocation_pools'][0]
    if (subnet['enable_dhcp'] != enable_dhcp):
        return True
    if (subnet_name and (subnet['name'] != subnet_name)):
        return True
    if (pool_start and (curr_pool['start'] != pool_start)):
        return True
    if (pool_end and (curr_pool['end'] != pool_end)):
        return True
    if (gateway_ip and (subnet['gateway_ip'] != gateway_ip)):
        return True
    if (dns and (sorted(subnet['dns_nameservers']) != sorted(dns))):
        return True
    if host_routes:
        curr_hr = sorted(subnet['host_routes'], key=(lambda t: t.keys()))
        new_hr = sorted(host_routes, key=(lambda t: t.keys()))
        if (sorted(curr_hr) != sorted(new_hr)):
            return True
    if (no_gateway_ip and subnet['gateway_ip']):
        return True
    return False