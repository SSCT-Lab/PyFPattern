def _exec(self, args, run_in_check_mode=False):
    if ((not self.module.check_mode) or run_in_check_mode):
        cmd = [self._rabbitmqctl, '-q']
        if (self.node is not None):
            cmd.extend(['-n', self.node])
        (rc, out, err) = self.module.run_command((cmd + args), check_rc=True)
        return (out.splitlines() if len(out.strip()) else [])
    return list()