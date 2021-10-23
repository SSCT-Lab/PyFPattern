def build_become_command(self, cmd, shell):
    super(BecomeModule, self).build_become_command(cmd, shell)
    if (not cmd):
        return cmd
    become_exe = (self.get_option('become_exe') or self.name)
    flags = (self.get_option('become_flags') or '')
    user = (self.get_option('become_user') or '')
    if user:
        user = ('-u %s' % user)
    noexe = (not self.get_option('wrap_exe'))
    return ' '.join([become_exe, flags, user, self._build_success_command(cmd, shell, noexe=noexe)])