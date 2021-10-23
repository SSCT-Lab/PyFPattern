def cli_get_stp_config(self):
    ' Cli get stp configuration '
    regular = '| include stp'
    flags = list()
    flags.append(regular)
    self.stp_cfg = get_config(self.module, flags)