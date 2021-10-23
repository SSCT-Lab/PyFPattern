def cli_add_command(self, command, undo=False):
    'add command to self.update_cmd and self.commands'
    self.commands.append('return')
    self.commands.append('mmi-mode enable')
    if (self.action == 'commit'):
        self.commands.append('sys')
    self.commands.append(command)
    self.updates_cmd.append(command)