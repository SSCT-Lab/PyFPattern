def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']), location=dict(type='str'), source=dict(type='str'), data_disk_sources=dict(type='list', default=[]), os_type=dict(type='str', choices=['Windows', 'Linux']))
    self.results = dict(changed=False, id=None)
    required_if = [('state', 'present', ['source'])]
    self.resource_group = None
    self.name = None
    self.state = None
    self.location = None
    self.source = None
    self.data_disk_sources = None
    self.os_type = None
    super(AzureRMImage, self).__init__(self.module_arg_spec, supports_check_mode=True, required_if=required_if)