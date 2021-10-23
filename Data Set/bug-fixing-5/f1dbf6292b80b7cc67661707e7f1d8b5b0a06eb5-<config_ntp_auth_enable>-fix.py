def config_ntp_auth_enable(self):
    'Config ntp authentication enable'
    commands = list()
    if (self.ntp_auth_conf['authentication'] != self.authentication):
        if (self.authentication == 'enable'):
            config_cli = 'ntp authentication enable'
        else:
            config_cli = 'undo ntp authentication enable'
        commands.append(config_cli)
        self.cli_load_config(commands)