def _upgrade_current_cask(self):
    command = 'upgrade'
    if (not self.valid_cask(self.current_cask)):
        self.failed = True
        self.message = 'Invalid cask: {0}.'.format(self.current_cask)
        raise HomebrewCaskException(self.message)
    if (not self._current_cask_is_installed()):
        command = 'install'
    if (self._current_cask_is_installed() and (not self._current_cask_is_outdated())):
        self.message = 'Cask is already upgraded: {0}'.format(self.current_cask)
        self.unchanged_count += 1
        return True
    if self.module.check_mode:
        self.changed = True
        self.message = 'Cask would be upgraded: {0}'.format(self.current_cask)
        raise HomebrewCaskException(self.message)
    opts = (([self.brew_path, 'cask', command] + self.install_options) + [self.current_cask])
    cmd = [opt for opt in opts if opt]
    (rc, out, err) = self.module.run_command(cmd)
    if (self._current_cask_is_installed() and (not self._current_cask_is_outdated())):
        self.changed_count += 1
        self.changed = True
        self.message = 'Cask upgraded: {0}'.format(self.current_cask)
        return True
    else:
        self.failed = True
        self.message = err.strip()
        raise HomebrewCaskException(self.message)