def write(self, backup_file=None):
    '\n        Write the crontab to the system. Saves all information.\n        '
    if backup_file:
        fileh = open(backup_file, 'w')
    elif self.cron_file:
        fileh = open(self.cron_file, 'w')
    else:
        (filed, path) = tempfile.mkstemp(prefix='crontab')
        os.chmod(path, int('0644', 8))
        fileh = os.fdopen(filed, 'w')
    fileh.write(self.render())
    fileh.close()
    if backup_file:
        return
    if (not self.cron_file):
        (rc, out, err) = self.module.run_command(self._write_execute(path), use_unsafe_shell=True)
        os.unlink(path)
        if (rc != 0):
            self.module.fail_json(msg=err)
    if HAS_SELINUX:
        selinux.selinux_lsetfilecon_default(self.cron_file)