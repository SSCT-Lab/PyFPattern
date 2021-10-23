def configure(self, commands, **kwargs):
    cmds = ['configure terminal']
    if (commands[(- 1)] == 'end'):
        commands.pop()
    cmds.extend(to_list(commands))
    cmds.extend(['commit', 'end'])
    responses = self.execute(cmds)
    return responses[1:]