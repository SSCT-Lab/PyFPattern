

def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), location=dict(type='str'), state=dict(type='str', default='present', choices=['present', 'absent']), sku=dict(type='str', choices=['standard_verizon', 'premium_verizon', 'custom_verizon', 'standard_akamai', 'standard_chinacdn', 'standard_microsoft']))
    self.resource_group = None
    self.name = None
    self.location = None
    self.state = None
    self.tags = None
    self.sku = None
    self.cdn_client = None
    required_if = [('state', 'present', ['sku'])]
    self.results = dict(changed=False)
    super(AzureRMCdnprofile, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True, required_if=required_if)
