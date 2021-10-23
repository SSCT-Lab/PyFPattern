def ssh_key_gen(self):
    info = self.user_info()
    try:
        ssh_key_file = self.get_ssh_key_path()
    except Exception:
        e = get_exception()
        return (1, '', str(e))
    ssh_dir = os.path.dirname(ssh_key_file)
    if (not os.path.exists(ssh_dir)):
        if self.module.check_mode:
            return (0, '', '')
        try:
            os.mkdir(ssh_dir, int('0700', 8))
            os.chown(ssh_dir, info[2], info[3])
        except OSError as e:
            return (1, '', ('Failed to create %s: %s' % (ssh_dir, to_native(e))))
    if os.path.exists(ssh_key_file):
        return (None, 'Key already exists', '')
    cmd = [self.module.get_bin_path('ssh-keygen', True)]
    cmd.append('-t')
    cmd.append(self.ssh_type)
    if (self.ssh_bits > 0):
        cmd.append('-b')
        cmd.append(self.ssh_bits)
    cmd.append('-C')
    cmd.append(self.ssh_comment)
    cmd.append('-f')
    cmd.append(ssh_key_file)
    cmd.append('-N')
    if (self.ssh_passphrase is not None):
        cmd.append(self.ssh_passphrase)
    else:
        cmd.append('')
    (rc, out, err) = self.execute_command(cmd)
    if ((rc == 0) and (not self.module.check_mode)):
        os.chown(ssh_key_file, info[2], info[3])
        os.chown(('%s.pub' % ssh_key_file), info[2], info[3])
    return (rc, out, err)