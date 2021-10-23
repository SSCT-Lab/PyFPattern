def init_module(self):
    ' init module '
    required_if = [('action', 'set', ['commit_id', 'label']), ('action', 'commit', ['label'])]
    mutually_exclusive = None
    required_one_of = None
    if (self.action == 'rollback'):
        required_one_of = [['commit_id', 'label', 'filename', 'last']]
    elif (self.action == 'clear'):
        required_one_of = [['commit_id', 'oldest']]
    self.module = AnsibleModule(argument_spec=self.spec, supports_check_mode=True, required_if=required_if, mutually_exclusive=mutually_exclusive, required_one_of=required_one_of)