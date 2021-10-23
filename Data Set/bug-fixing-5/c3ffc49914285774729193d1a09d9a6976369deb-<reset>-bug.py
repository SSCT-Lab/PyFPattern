def reset(self):
    cmd = map(to_bytes, self._build_command(self._play_context.ssh_executable, '-O', 'stop', self.host))
    (controlpersist, controlpath) = self._persistence_controls(cmd)
    if controlpersist:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        display.vvv(('sending stop: %s' % cmd))
    self.close()