def reset(self):
    cmd = self._build_command(self._play_context.ssh_executable, '-O', 'stop', self.host)
    (controlpersist, controlpath) = self._persistence_controls(cmd)
    cp_arg = [a for a in cmd if a.startswith(b'ControlPath=')]
    run_reset = False
    if (controlpersist and (len(cp_arg) > 0)):
        cp_path = cp_arg[0].split(b'=', 1)[(- 1)]
        if os.path.exists(cp_path):
            run_reset = True
    elif controlpersist:
        run_reset = True
    if run_reset:
        display.vvv(('sending stop: %s' % cmd))
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        status_code = p.wait()
        if (status_code != 0):
            display.warning(('Failed to reset connection:%s' % stderr))
    self.close()