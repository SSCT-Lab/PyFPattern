def get_jumboframe_config(self):
    ' get_jumboframe_config'
    flags = list()
    exp = ('| ignore-case section include ^#\\s+interface %s\\s+' % self.interface.replace(' ', ''))
    flags.append(exp)
    output = self.get_config(flags)
    output = output.replace('*', '').lower()
    return self.prase_jumboframe_para(output)