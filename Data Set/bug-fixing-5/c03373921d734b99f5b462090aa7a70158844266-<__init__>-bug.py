def __init__(self):
    self.module_arg_spec = dict(default_rules=dict(type='list', elements='dict', options=rule_spec), location=dict(type='str'), name=dict(type='str', required=True), purge_default_rules=dict(type='bool', default=False), purge_rules=dict(type='bool', default=False), resource_group=dict(required=True, type='str'), rules=dict(type='list', elements='dict', options=rule_spec), state=dict(type='str', default='present', choices=['present', 'absent']))
    self.default_rules = None
    self.location = None
    self.name = None
    self.purge_default_rules = None
    self.purge_rules = None
    self.resource_group = None
    self.rules = None
    self.state = None
    self.tags = None
    self.client = None
    self.nsg_models = None
    self.results = dict(changed=False, state=dict())
    super(AzureRMSecurityGroup, self).__init__(self.module_arg_spec, supports_check_mode=True)