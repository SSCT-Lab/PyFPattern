

def build_become_command(self, cmd, shell):
    super(BecomeModule, self).build_become_command(cmd, shell)
    if (not cmd):
        return cmd
    become = (self._get_option('become_exe') or self.name)
    flags = (self.get_option('flags') or '')
    user = (self.get_option('become_user') or '')
    return ('%s shell -q %s %s@ -- %s' % (become, flags, user, cmd))
