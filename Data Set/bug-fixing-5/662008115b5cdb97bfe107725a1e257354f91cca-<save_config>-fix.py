def save_config(self):
    cmdlist = list()
    cmd = 'copy running-config startup-config'
    cmdlist.append(Command(cmd, prompt=self.WARNING_PROMPTS_RE, response='yes'))
    self.execute(cmdlist)