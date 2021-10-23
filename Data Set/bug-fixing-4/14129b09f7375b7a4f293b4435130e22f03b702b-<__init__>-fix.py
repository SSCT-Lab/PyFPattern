def __init__(self):
    self.module_arg_spec = dict(name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']), location=dict(type='str'), force_delete_nonempty=dict(type='bool', default=False, aliases=['force']))
    self.name = None
    self.state = None
    self.location = None
    self.tags = None
    self.force_delete_nonempty = None
    self.results = dict(changed=False, contains_resources=False, state=dict())
    super(AzureRMResourceGroup, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)