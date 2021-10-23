def _build_static(self):
    env = dict(os.environ)
    env['SENTRY_STATIC_DIST_PATH'] = self.sentry_static_dist_path
    env['NODE_ENV'] = 'production'
    self._run_yarn_command(['webpack', '--bail'], env=env)