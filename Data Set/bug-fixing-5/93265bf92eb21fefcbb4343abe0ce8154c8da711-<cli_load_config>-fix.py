def cli_load_config(self):
    'load config by cli'
    if (not self.module.check_mode):
        if (len(self.commands) > 1):
            load_config(self.module, self.commands)
            self.changed = True