def _run_yarn_command(self, cmd, env=None):
    log.debug('yarn path: ({0})'.format(YARN_PATH))
    self._run_command(([YARN_PATH] + cmd), env=env)