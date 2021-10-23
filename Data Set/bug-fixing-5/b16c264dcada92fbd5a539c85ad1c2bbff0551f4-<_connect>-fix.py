def _connect(self):
    ' connect to the chroot '
    if os.path.isabs(self.get_option('chroot_exe')):
        self.chroot_cmd = self.get_option('chroot_exe')
    else:
        self.chroot_cmd = get_bin_path(self.get_option('chroot_exe'))
    if (not self.chroot_cmd):
        raise AnsibleError(('chroot command (%s) not found in PATH' % to_native(self.get_option('chroot_exe'))))
    super(Connection, self)._connect()
    if (not self._connected):
        display.vvv('THIS IS A LOCAL CHROOT DIR', host=self.chroot)
        self._connected = True