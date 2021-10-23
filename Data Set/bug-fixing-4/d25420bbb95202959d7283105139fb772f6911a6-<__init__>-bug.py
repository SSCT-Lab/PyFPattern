def __init__(self):
    self.module_args = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']), location=dict(type='str'), sku=dict(type='str', choices=['Basic', 'Standard']), frontend_ip_configurations=dict(type='list', elements='dict', options=frontend_ip_configuration_spec), backend_address_pools=dict(type='list', elements='dict', options=backend_address_pool_spec), probes=dict(type='list', elements='dict', options=probes_spec), inbound_nat_pools=dict(type='list', elements='dict', options=inbound_nat_pool_spec), load_balancing_rules=dict(type='list', elements='dict', options=load_balancing_rule_spec), public_ip_address_name=dict(type='str', aliases=['public_ip_address', 'public_ip_name', 'public_ip']), probe_port=dict(type='int'), probe_protocol=dict(type='str', choices=['Tcp', 'Http']), probe_interval=dict(type='int', default=15), probe_fail_count=dict(type='int', default=3), probe_request_path=dict(type='str'), protocol=dict(type='str', choices=['Tcp', 'Udp']), load_distribution=dict(type='str', choices=['Default', 'SourceIP', 'SourceIPProtocol']), frontend_port=dict(type='int'), backend_port=dict(type='int'), idle_timeout=dict(type='int', default=4), natpool_frontend_port_start=dict(type='int'), natpool_frontend_port_end=dict(type='int'), natpool_backend_port=dict(type='int'), natpool_protocol=dict(type='str'))
    self.resource_group = None
    self.name = None
    self.location = None
    self.sku = None
    self.frontend_ip_configurations = None
    self.backend_address_pools = None
    self.probes = None
    self.inbound_nat_pools = None
    self.load_balancing_rules = None
    self.public_ip_address_name = None
    self.state = None
    self.probe_port = None
    self.probe_protocol = None
    self.probe_interval = None
    self.probe_fail_count = None
    self.probe_request_path = None
    self.protocol = None
    self.load_distribution = None
    self.frontend_port = None
    self.backend_port = None
    self.idle_timeout = None
    self.natpool_frontend_port_start = None
    self.natpool_frontend_port_end = None
    self.natpool_backend_port = None
    self.natpool_protocol = None
    self.results = dict(changed=False, state=dict())
    super(AzureRMLoadBalancer, self).__init__(derived_arg_spec=self.module_args, supports_check_mode=True)