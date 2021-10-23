def init_module(self):
    'Init module object'
    required_if = [('state', 'present', ('auth_pwd', 'auth_mode'))]
    self.module = AnsibleModule(argument_spec=self.spec, required_if=required_if, supports_check_mode=True)