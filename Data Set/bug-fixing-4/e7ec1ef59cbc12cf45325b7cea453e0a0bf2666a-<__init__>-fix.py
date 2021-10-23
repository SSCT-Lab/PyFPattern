def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), os_type=dict(type='str', default='linux', choices=['linux', 'windows']), state=dict(type='str', default='present', choices=['present', 'absent']), location=dict(type='str'), ip_address=dict(type='str', default='none', choices=['public', 'none']), ports=dict(type='list', default=[]), registry_login_server=dict(type='str', default=None), registry_username=dict(type='str', default=None), registry_password=dict(type='str', default=None, no_log=True), containers=dict(type='list', required=True), force_update=dict(type='bool', default=False))
    self.resource_group = None
    self.name = None
    self.location = None
    self.state = None
    self.ip_address = None
    self.containers = None
    self.tags = None
    self.results = dict(changed=False, state=dict())
    self.cgmodels = None
    super(AzureRMContainerInstance, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True)