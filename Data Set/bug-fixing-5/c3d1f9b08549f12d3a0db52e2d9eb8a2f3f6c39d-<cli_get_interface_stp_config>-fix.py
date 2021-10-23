def cli_get_interface_stp_config(self):
    " Cli get interface's stp configuration "
    if self.interface:
        regular = ('| ignore-case section include ^#\\s+interface %s\\s+' % self.interface.replace(' ', ''))
        flags = list()
        flags.append(regular)
        tmp_cfg = get_config(self.module, flags)
        if (not tmp_cfg):
            self.module.fail_json(msg=('Error: The interface %s is not exist.' % self.interface))
        if ('undo portswitch' in tmp_cfg):
            self.module.fail_json(msg=('Error: The interface %s is not switch mode.' % self.interface))
        self.interface_stp_cfg = tmp_cfg