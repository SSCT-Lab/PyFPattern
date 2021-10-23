def undo_config_ntp_auth_keyid(self):
    'Undo ntp authentication key-id'
    commands = list()
    config_cli = ('undo ntp authentication-keyid %s' % self.key_id)
    commands.append(config_cli)
    self.cli_load_config(commands)