def get_jumboframe_config(self):
    ' get_jumboframe_config'
    flags = list()
    exp = (' all | section inc %s$' % self.interface.upper())
    flags.append(exp)
    output = get_config(self.module, flags)
    output = output.replace('*', '')
    return self.prase_jumboframe_para(output)