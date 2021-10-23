def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str'))
    self.results = dict()
    self.resource_group = None
    self.name = None
    self.tags = None
    super(AzureRMAutoScaleFacts, self).__init__(self.module_arg_spec)