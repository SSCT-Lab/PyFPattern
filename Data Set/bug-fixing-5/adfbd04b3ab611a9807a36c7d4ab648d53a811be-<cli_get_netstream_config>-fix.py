def cli_get_netstream_config(self):
    ' Cli get netstream configuration '
    if (self.type == 'ip'):
        cmd = ('netstream record %s ip' % self.record_name)
    else:
        cmd = ('netstream record %s vxlan inner-ip' % self.record_name)
    flags = list()
    regular = ('| section include %s' % cmd)
    flags.append(regular)
    self.netstream_cfg = get_config(self.module, flags)