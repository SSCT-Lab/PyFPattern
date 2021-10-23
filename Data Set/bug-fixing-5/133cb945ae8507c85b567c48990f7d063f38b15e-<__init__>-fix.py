def __init__(self, argument_spec):
    self.spec = argument_spec
    self.module = AnsibleModule(argument_spec=self.spec, supports_check_mode=True)
    self.commands = list()
    self.commit_id = self.module.params['commit_id']
    self.label = self.module.params['label']
    self.filename = self.module.params['filename']
    self.last = self.module.params['last']
    self.oldest = self.module.params['oldest']
    self.action = self.module.params['action']
    self.changed = False
    self.updates_cmd = list()
    self.results = dict()
    self.existing = dict()
    self.proposed = dict()
    self.end_state = dict()
    self.rollback_info = None
    self.init_module()