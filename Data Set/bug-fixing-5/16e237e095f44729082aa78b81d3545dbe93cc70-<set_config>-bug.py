def set_config(self):
    if (self.action == 'rollback'):
        if self.commit_id:
            cmd = ('rollback configuration to commit-id %s' % self.commit_id)
            cmd = {
                'command': cmd,
                'prompt': '[Y/N]',
                'answer': 'Y',
            }
            self.cli_add_command(cmd)
        if self.label:
            cmd = ('rollback configuration to label %s' % self.label)
            cmd = {
                'command': cmd,
                'prompt': '[Y/N]',
                'answer': 'Y',
            }
            self.cli_add_command(cmd)
        if self.filename:
            cmd = ('rollback configuration to file %s' % self.filename)
            cmd = {
                'command': cmd,
                'prompt': '[Y/N]',
                'answer': 'Y',
            }
            self.cli_add_command(cmd)
        if self.last:
            cmd = ('rollback configuration last %s' % self.last)
            cmd = {
                'command': cmd,
                'prompt': '[Y/N]',
                'answer': 'Y',
            }
            self.cli_add_command(cmd)
    elif (self.action == 'set'):
        if (self.commit_id and self.label):
            cmd = ('set configuration commit %s label %s' % (self.commit_id, self.label))
            self.cli_add_command(cmd)
    elif (self.action == 'clear'):
        if self.commit_id:
            cmd = ('clear configuration commit %s label' % self.commit_id)
            self.cli_add_command(cmd)
        if self.oldest:
            cmd = ('clear configuration commit oldest %s' % self.oldest)
            cmd = {
                'command': cmd,
                'prompt': '[Y/N]',
                'answer': 'Y',
            }
            self.cli_add_command(cmd)
    elif (self.action == 'commit'):
        if self.label:
            cmd = ('commit label %s' % self.label)
            self.cli_add_command(cmd)
    elif (self.action == 'display'):
        self.rollback_info = self.get_rollback_dict()
    if self.commands:
        self.cli_load_config(self.commands)
        self.changed = True