def install_bundle(self, bundle):
    'Installs a bundle with `swupd bundle-add bundle`'
    if self.module.check_mode:
        self.module.exit_json(changed=(not self._is_bundle_installed(bundle)))
    if self._is_bundle_installed(bundle):
        self.msg = ('Bundle %s is already installed' % bundle)
        return
    cmd = self._get_cmd(('bundle-add %s' % bundle))
    self._run_cmd(cmd)
    if (self.rc == 0):
        self.changed = True
        self.msg = ('Bundle %s installed' % bundle)
        return
    if (self.rc == 18):
        self.msg = ('Bundle name %s is invalid' % bundle)
        return
    self.failed = True
    self.msg = ('Failed to install bundle %s' % bundle)