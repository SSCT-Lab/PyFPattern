def init_module(self):
    ' init module '
    self.module = AnsibleModule(argument_spec=self.spec, supports_check_mode=True)