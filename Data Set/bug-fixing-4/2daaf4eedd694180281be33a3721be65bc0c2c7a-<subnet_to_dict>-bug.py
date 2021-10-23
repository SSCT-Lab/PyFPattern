def subnet_to_dict(subnet):
    result = dict(id=subnet.id, name=subnet.name, provisioning_state=subnet.provisioning_state, address_prefix=subnet.address_prefix, network_security_group=dict(), route_table=dict())
    if subnet.network_security_group:
        id_keys = azure_id_to_dict(subnet.network_security_group.id)
        result['network_security_group']['id'] = subnet.network_security_group.id
        result['network_security_group']['name'] = id_keys['networkSecurityGroups']
        result['network_security_group']['resource_group'] = id_keys['resourceGroups']
    if subnet.route_table:
        id_keys = azure_id_to_dict(subnet.route_table.id)
        result['route_table']['id'] = subnet.route_table.id
        result['route_table']['name'] = id_keys['routeTables']
        result['route_table']['resource_group'] = id_keys['resourceGroups']
    if subnet.service_endpoints:
        result['service_endpoints'] = [{
            'service': item.service,
            'locations': item.locations,
        } for item in subnet.service_endpoints]
    return result