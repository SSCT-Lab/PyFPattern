def cli_load_config(self, commands):
    ' Cli method to load config '
    if (not self.module.check_mode):
        load_config(self.module, commands)