def configure(self, commands, **kwargs):
    cmds = ['configure terminal']
    cmds.extend(to_list(commands))
    responses = self.execute(cmds)
    return responses[1:]