

def _needs_update(cloud, module, router, network, internal_subnet_ids, internal_port_ids):
    'Decide if the given router needs an update.\n    '
    if (router['admin_state_up'] != module.params['admin_state_up']):
        return True
    if router['external_gateway_info']:
        if (module.params['enable_snat'] is not None):
            if (router['external_gateway_info'].get('enable_snat', True) != module.params['enable_snat']):
                return True
    if network:
        if (not router['external_gateway_info']):
            return True
        elif (router['external_gateway_info']['network_id'] != network['id']):
            return True
    if module.params['external_fixed_ips']:
        for new_iface in module.params['external_fixed_ips']:
            subnet = cloud.get_subnet(new_iface['subnet'])
            exists = False
            for existing_iface in router['external_gateway_info']['external_fixed_ips']:
                if (existing_iface['subnet_id'] == subnet['id']):
                    if ('ip' in new_iface):
                        if (existing_iface['ip_address'] == new_iface['ip']):
                            exists = True
                            break
                    else:
                        exists = True
                        break
            if (not exists):
                return True
    if module.params['interfaces']:
        existing_subnet_ids = []
        for port in _router_internal_interfaces(cloud, router):
            if ('fixed_ips' in port):
                for fixed_ip in port['fixed_ips']:
                    existing_subnet_ids.append(fixed_ip['subnet_id'])
        for iface in module.params['interfaces']:
            if isinstance(iface, dict):
                for p_id in internal_port_ids:
                    p = cloud.get_port(name_or_id=p_id)
                    if ('fixed_ips' in p):
                        for fip in p['fixed_ips']:
                            internal_subnet_ids.append(fip['subnet_id'])
        if (set(internal_subnet_ids) != set(existing_subnet_ids)):
            internal_subnet_ids = []
            return True
    return False
