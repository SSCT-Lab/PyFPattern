def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']), location=dict(type='str'), virtual_machine_name=dict(type='str'), publisher=dict(type='str'), virtual_machine_extension_type=dict(type='str'), type_handler_version=dict(type='str'), auto_upgrade_minor_version=dict(type='bool'), settings=dict(type='dict'), protected_settings=dict(type='dict'))
    self.resource_group = None
    self.name = None
    self.location = None
    self.publisher = None
    self.virtual_machine_extension_type = None
    self.type_handler_version = None
    self.auto_upgrade_minor_version = None
    self.settings = None
    self.protected_settings = None
    self.state = None
    self.results = dict(changed=False, state=dict())
    super(AzureRMVMExtension, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=False, supports_tags=False)