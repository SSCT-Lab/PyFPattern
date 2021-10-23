def _build_kwargs(cloud, module, router, network):
    kwargs = {
        'admin_state_up': module.params['admin_state_up'],
    }
    if router:
        kwargs['name_or_id'] = router['id']
    else:
        kwargs['name'] = module.params['name']
    if network:
        kwargs['ext_gateway_net_id'] = network['id']
        if (module.params.get('enable_snat') is not None):
            kwargs['enable_snat'] = module.params['enable_snat']
    if module.params['external_fixed_ips']:
        kwargs['ext_fixed_ips'] = []
        for iface in module.params['external_fixed_ips']:
            subnet = cloud.get_subnet(iface['subnet'])
            d = {
                'subnet_id': subnet['id'],
            }
            if ('ip' in iface):
                d['ip_address'] = iface['ip']
            kwargs['ext_fixed_ips'].append(d)
    return kwargs