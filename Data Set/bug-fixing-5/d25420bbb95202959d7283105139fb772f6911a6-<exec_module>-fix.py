def exec_module(self, **kwargs):
    'Main module execution method'
    for key in (list(self.module_args.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    changed = False
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    load_balancer = self.get_load_balancer()
    if (self.state == 'present'):
        if ((not self.frontend_ip_configurations) and (not self.backend_address_pools) and (not self.probes) and (not self.inbound_nat_pools)):
            self.deprecate('Discrete load balancer config settings are deprecated and will be removed. Use frontend_ip_configurations, backend_address_pools, probes, inbound_nat_pools lists instead.', version='2.9')
            frontend_ip_name = 'frontendip0'
            backend_address_pool_name = 'backendaddrp0'
            prob_name = 'prob0'
            inbound_nat_pool_name = 'inboundnatp0'
            lb_rule_name = 'lbr'
            self.frontend_ip_configurations = [dict(name=frontend_ip_name, public_ip_address=self.public_ip_address_name)]
            self.backend_address_pools = [dict(name=backend_address_pool_name)]
            self.probes = ([dict(name=prob_name, port=self.probe_port, protocol=self.probe_protocol, interval=self.probe_interval, fail_count=self.probe_fail_count, request_path=self.probe_request_path)] if self.probe_protocol else None)
            self.inbound_nat_pools = ([dict(name=inbound_nat_pool_name, frontend_ip_configuration_name=frontend_ip_name, protocol=self.natpool_protocol, frontend_port_range_start=self.natpool_frontend_port_start, frontend_port_range_end=self.natpool_frontend_port_end, backend_port=self.natpool_backend_port)] if self.natpool_protocol else None)
            self.load_balancing_rules = ([dict(name=lb_rule_name, frontend_ip_configuration=frontend_ip_name, backend_address_pool=backend_address_pool_name, probe=prob_name, protocol=self.protocol, load_distribution=self.load_distribution, frontend_port=self.frontend_port, backend_port=self.backend_port, idle_timeout=self.idle_timeout, enable_floating_ip=False)] if self.protocol else None)
        if load_balancer:
            changed = False
        else:
            changed = True
    elif ((self.state == 'absent') and load_balancer):
        changed = True
    self.results['state'] = load_balancer_to_dict(load_balancer)
    if ('tags' in self.results['state']):
        (update_tags, self.results['state']['tags']) = self.update_tags(self.results['state']['tags'])
        if update_tags:
            changed = True
    elif self.tags:
        changed = True
    self.results['changed'] = changed
    if ((self.state == 'present') and changed):
        frontend_ip_configurations_param = ([self.network_models.FrontendIPConfiguration(name=item.get('name'), public_ip_address=(self.get_public_ip_address_instance(item.get('public_ip_address')) if item.get('public_ip_address') else None), private_ip_address=item.get('private_ip_address'), private_ip_allocation_method=item.get('private_ip_allocation_method'), subnet=(self.network_models.Subnet(id=item.get('subnet')) if item.get('subnet') else None)) for item in self.frontend_ip_configurations] if self.frontend_ip_configurations else None)
        backend_address_pools_param = ([self.network_models.BackendAddressPool(name=item.get('name')) for item in self.backend_address_pools] if self.backend_address_pools else None)
        probes_param = ([self.network_models.Probe(name=item.get('name'), port=item.get('port'), protocol=item.get('protocol'), interval_in_seconds=item.get('interval'), request_path=item.get('request_path'), number_of_probes=item.get('fail_count')) for item in self.probes] if self.probes else None)
        inbound_nat_pools_param = ([self.network_models.InboundNatPool(name=item.get('name'), frontend_ip_configuration=self.network_models.SubResource(frontend_ip_configuration_id(self.subscription_id, self.resource_group, self.name, item.get('frontend_ip_configuration_name'))), protocol=item.get('protocol'), frontend_port_range_start=item.get('frontend_port_range_start'), frontend_port_range_end=item.get('frontend_port_range_end'), backend_port=item.get('backend_port')) for item in self.inbound_nat_pools] if self.inbound_nat_pools else None)
        load_balancing_rules_param = ([self.network_models.LoadBalancingRule(name=item.get('name'), frontend_ip_configuration=self.network_models.SubResource(frontend_ip_configuration_id(self.subscription_id, self.resource_group, self.name, item.get('frontend_ip_configuration'))), backend_address_pool=self.network_models.SubResource(backend_address_pool_id(self.subscription_id, self.resource_group, self.name, item.get('backend_address_pool'))), probe=self.network_models.SubResource(probe_id(self.subscription_id, self.resource_group, self.name, item.get('probe'))), protocol=item.get('protocol'), load_distribution=item.get('load_distribution'), frontend_port=item.get('frontend_port'), backend_port=item.get('backend_port'), idle_timeout_in_minutes=item.get('idle_timeout'), enable_floating_ip=item.get('enable_floating_ip')) for item in self.load_balancing_rules] if self.load_balancing_rules else None)
        param = self.network_models.LoadBalancer(sku=(self.network_models.LoadBalancerSku(self.sku) if self.sku else None), location=self.location, tags=self.tags, frontend_ip_configurations=frontend_ip_configurations_param, backend_address_pools=backend_address_pools_param, probes=probes_param, inbound_nat_pools=inbound_nat_pools_param, load_balancing_rules=load_balancing_rules_param)
        self.results['state'] = self.create_or_update_load_balancer(param)
    elif ((self.state == 'absent') and changed):
        self.delete_load_balancer()
        self.results['state'] = None
    return self.results