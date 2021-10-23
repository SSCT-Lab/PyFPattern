def _run(self):
    if self.update_homebrew:
        self._update_homebrew()
    if (self.state == 'installed'):
        return self._install_casks()
    elif (self.state == 'absent'):
        return self._uninstall_casks()
    if self.command:
        return self._command()