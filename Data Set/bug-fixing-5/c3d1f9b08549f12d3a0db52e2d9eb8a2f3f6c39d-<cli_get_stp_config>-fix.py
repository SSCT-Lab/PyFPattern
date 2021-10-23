def cli_get_stp_config(self):
    ' Cli get stp configuration '
    flags = ['| section include #\\s*\\n\\s*stp', '| section exclude #\\s*\\n+\\s*stp process \\d+']
    self.stp_cfg = get_config(self.module, flags)