def config_ntp_auth(self):
    'Config ntp authentication'
    if (self.state == 'present'):
        self.config_ntp_auth_keyid()
    else:
        if (not self.key_id_exist):
            self.module.fail_json(msg='Error: The Authentication-keyid does not exist.')
        self.undo_config_ntp_auth_keyid()
    if self.authentication:
        self.config_ntp_auth_enable()
    self.changed = True