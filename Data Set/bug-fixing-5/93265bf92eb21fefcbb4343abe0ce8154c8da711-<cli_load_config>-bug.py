def cli_load_config(self, commands):
    'load config by cli'
    if (not self.module.check_mode):
        load_config(self.module, commands)