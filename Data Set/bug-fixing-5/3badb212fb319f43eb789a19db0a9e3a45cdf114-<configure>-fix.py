def configure(self, commands, **kwargs):
    cmds = ['configure terminal']
    cmds.extend(to_list(commands))
    cmds.append('end')
    responses = self.execute(cmds)
    return responses[1:(- 1)]