def _run(self):
    if self.upgrade_all:
        return self._upgrade_all()
    if self.casks:
        if (self.state == 'installed'):
            return self._install_casks()
        elif (self.state == 'upgraded'):
            return self._upgrade_casks()
        elif (self.state == 'absent'):
            return self._uninstall_casks()
    self.failed = True
    self.message = 'You must select a cask to install.'
    raise HomebrewCaskException(self.message)