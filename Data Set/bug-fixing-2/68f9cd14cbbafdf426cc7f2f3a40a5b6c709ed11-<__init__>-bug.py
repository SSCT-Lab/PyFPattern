

def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), sku=dict(type='dict'), location=dict(type='str'), storage_mb=dict(type='int'), version=dict(type='str', choices=['9.5', '9.6', '10']), enforce_ssl=dict(type='bool', default=False), create_mode=dict(type='str', default='Default'), admin_username=dict(type='str'), admin_password=dict(type='str', no_log=True), state=dict(type='str', default='present', choices=['present', 'absent']))
    self.resource_group = None
    self.name = None
    self.parameters = dict()
    self.tags = None
    self.results = dict(changed=False)
    self.state = None
    self.to_do = Actions.NoAction
    super(AzureRMPostgreSqlServers, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True)
