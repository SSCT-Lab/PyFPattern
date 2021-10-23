def init_module(self):
    ' init module '
    required_if = [('state', 'absent', ['mode']), ('state', 'present', ['mode'])]
    self.module = AnsibleModule(argument_spec=self.spec, required_if=required_if, supports_check_mode=True)