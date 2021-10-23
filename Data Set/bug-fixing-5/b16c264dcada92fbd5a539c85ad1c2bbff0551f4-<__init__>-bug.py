def __init__(self, play_context, new_stdin, *args, **kwargs):
    super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)
    self.chroot = self._play_context.remote_addr
    if (os.geteuid() != 0):
        raise AnsibleError('chroot connection requires running as root')
    if (not os.path.isdir(self.chroot)):
        raise AnsibleError(('%s is not a directory' % self.chroot))
    chrootsh = os.path.join(self.chroot, 'bin/sh')
    if (not (is_executable(chrootsh) or (os.path.lexists(chrootsh) and os.path.islink(chrootsh)))):
        raise AnsibleError(('%s does not look like a chrootable dir (/bin/sh missing)' % self.chroot))
    if os.path.isabs(self.get_option('chroot_exe')):
        self.chroot_cmd = self.get_option('chroot_exe')
    else:
        self.chroot_cmd = get_bin_path(self.get_option('chroot_exe'))
    if (not self.chroot_cmd):
        raise AnsibleError(('chroot command (%s) not found in PATH' % to_native(self.get_option('chroot_exe'))))