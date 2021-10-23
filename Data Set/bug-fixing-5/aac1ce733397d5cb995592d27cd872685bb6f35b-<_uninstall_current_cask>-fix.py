def _uninstall_current_cask(self):
    if (not self.valid_cask(self.current_cask)):
        self.failed = True
        self.message = 'Invalid cask: {0}.'.format(self.current_cask)
        raise HomebrewCaskException(self.message)
    if (not self._current_cask_is_installed()):
        self.unchanged_count += 1
        self.message = 'Cask already uninstalled: {0}'.format(self.current_cask)
        return True
    if self.module.check_mode:
        self.changed = True
        self.message = 'Cask would be uninstalled: {0}'.format(self.current_cask)
        raise HomebrewCaskException(self.message)
    opts = ([self.brew_path, 'cask', 'uninstall', self.current_cask] + self.install_options)
    cmd = [opt for opt in opts if opt]
    (rc, out, err) = self.module.run_command(cmd)
    if (not self._current_cask_is_installed()):
        self.changed_count += 1
        self.changed = True
        self.message = 'Cask uninstalled: {0}'.format(self.current_cask)
        return True
    else:
        self.failed = True
        self.message = err.strip()
        raise HomebrewCaskException(self.message)