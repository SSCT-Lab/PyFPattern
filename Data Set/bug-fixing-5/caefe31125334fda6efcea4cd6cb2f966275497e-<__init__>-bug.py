def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']), virtual_network_name=dict(type='str', required=True, aliases=['virtual_network']), address_prefix_cidr=dict(type='str', aliases=['address_prefix']), security_group_name=dict(type='str', aliases=['security_group']))
    required_if = [('state', 'present', ['address_prefix_cidr'])]
    self.results = dict(changed=False, state=dict())
    self.resource_group = None
    self.name = None
    self.state = None
    self.virtual_etwork_name = None
    self.address_prefix_cidr = None
    self.security_group_name = None
    super(AzureRMSubnet, self).__init__(self.module_arg_spec, supports_check_mode=True, required_if=required_if)