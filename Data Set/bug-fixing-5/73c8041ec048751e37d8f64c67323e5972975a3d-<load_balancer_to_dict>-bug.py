def load_balancer_to_dict(load_balancer):
    'Seralialize a LoadBalancer object to a dict'
    if (not load_balancer):
        return dict()
    result = dict(id=load_balancer.id, name=load_balancer.name, location=load_balancer.location, sku=load_balancer.sku.name, tags=load_balancer.tags, provisioning_state=load_balancer.provisioning_state, etag=load_balancer.etag, frontend_ip_configurations=[], backend_address_pools=[], load_balancing_rules=[], probes=[], inbound_nat_rules=[], inbound_nat_pools=[], outbound_nat_rules=[])
    if load_balancer.frontend_ip_configurations:
        result['frontend_ip_configurations'] = [dict(id=_.id, name=_.name, etag=_.etag, provisioning_state=_.provisioning_state, private_ip_address=_.private_ip_address, private_ip_allocation_method=_.private_ip_allocation_method, subnet=(dict(id=_.subnet.id, name=_.subnet.name, address_prefix=_.subnet.address_prefix) if _.subnet else None), public_ip_address=(dict(id=_.public_ip_address.id, location=_.public_ip_address.location, public_ip_allocation_method=_.public_ip_address.public_ip_allocation_method, ip_address=_.public_ip_address.ip_address) if _.public_ip_address else None)) for _ in load_balancer.frontend_ip_configurations]
    if load_balancer.backend_address_pools:
        result['backend_address_pools'] = [dict(id=_.id, name=_.name, provisioning_state=_.provisioning_state, etag=_.etag) for _ in load_balancer.backend_address_pools]
    if load_balancer.load_balancing_rules:
        result['load_balancing_rules'] = [dict(id=_.id, name=_.name, protocol=_.protocol, frontend_ip_configuration_id=_.frontend_ip_configuration.id, backend_address_pool_id=_.backend_address_pool.id, probe_id=_.probe.id, load_distribution=_.load_distribution, frontend_port=_.frontend_port, backend_port=_.backend_port, idle_timeout_in_minutes=_.idle_timeout_in_minutes, enable_floating_ip=_.enable_floating_ip, provisioning_state=_.provisioning_state, etag=_.etag) for _ in load_balancer.load_balancing_rules]
    if load_balancer.probes:
        result['probes'] = [dict(id=_.id, name=_.name, protocol=_.protocol, port=_.port, interval_in_seconds=_.interval_in_seconds, number_of_probes=_.number_of_probes, request_path=_.request_path, provisioning_state=_.provisioning_state) for _ in load_balancer.probes]
    if load_balancer.inbound_nat_rules:
        result['inbound_nat_rules'] = [dict(id=_.id, name=_.name, frontend_ip_configuration_id=_.frontend_ip_configuration.id, protocol=_.protocol, frontend_port=_.frontend_port, backend_port=_.backend_port, idle_timeout_in_minutes=_.idle_timeout_in_minutes, enable_floating_point_ip=_.enable_floating_point_ip, provisioning_state=_.provisioning_state, etag=_.etag) for _ in load_balancer.inbound_nat_rules]
    if load_balancer.inbound_nat_pools:
        result['inbound_nat_pools'] = [dict(id=_.id, name=_.name, frontend_ip_configuration_id=_.frontend_ip_configuration.id, protocol=_.protocol, frontend_port_range_start=_.frontend_port_range_start, frontend_port_range_end=_.frontend_port_range_end, backend_port=_.backend_port, provisioning_state=_.provisioning_state, etag=_.etag) for _ in load_balancer.inbound_nat_pools]
    if load_balancer.outbound_nat_rules:
        result['outbound_nat_rules'] = [dict(id=_.id, name=_.name, allocated_outbound_ports=_.allocated_outbound_ports, frontend_ip_configuration_id=_.frontend_ip_configuration.id, backend_address_pool=_.backend_address_pool.id, provisioning_state=_.provisioning_state, etag=_.etag) for _ in load_balancer.outbound_nat_rules]
    return result