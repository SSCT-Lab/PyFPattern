def __init__(self):
    self.module_arg_spec = dict(account_type=dict(type='str', choices=[], aliases=['type']), custom_domain=dict(type='dict'), location=dict(type='str'), name=dict(type='str', required=True), resource_group=dict(required=True, type='str', aliases=['resource_group_name']), state=dict(default='present', choices=['present', 'absent']), force=dict(type='bool', default=False), tags=dict(type='dict'), kind=dict(type='str', default='Storage', choices=['Storage', 'BlobStorage']))
    for key in SkuName:
        self.module_arg_spec['account_type']['choices'].append(getattr(key, 'value'))
    self.results = dict(changed=False, state=dict())
    self.account_dict = None
    self.resource_group = None
    self.name = None
    self.state = None
    self.location = None
    self.account_type = None
    self.custom_domain = None
    self.tags = None
    self.force = None
    self.kind = None
    super(AzureRMStorageAccount, self).__init__(self.module_arg_spec, supports_check_mode=True)