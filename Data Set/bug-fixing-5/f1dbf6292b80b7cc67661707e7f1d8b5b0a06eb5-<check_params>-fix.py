def check_params(self):
    'Check all input params'
    if (not self.key_id.isdigit()):
        self.module.fail_json(msg='Error: key_id is not digit.')
    if ((int(self.key_id) < 1) or (int(self.key_id) > 4294967295)):
        self.module.fail_json(msg='Error: The length of key_id is between 1 and 4294967295.')
    if ((self.state == 'present') and (not self.password)):
        self.module.fail_json(msg='Error: The password cannot be empty.')
    if ((self.state == 'present') and self.password):
        if ((self.auth_type == 'encrypt') and ((len(self.password) < 20) or (len(self.password) > 392))):
            self.module.fail_json(msg='Error: The length of encrypted password is between 20 and 392.')
        elif ((self.auth_type == 'text') and ((len(self.password) < 1) or (len(self.password) > 255))):
            self.module.fail_json(msg='Error: The length of text password is between 1 and 255.')