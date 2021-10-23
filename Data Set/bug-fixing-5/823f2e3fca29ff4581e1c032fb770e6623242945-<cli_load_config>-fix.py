def cli_load_config(self, commands):
    ' Cli method to load config '
    if (not self.module.check_mode):
        self.load_config(commands)