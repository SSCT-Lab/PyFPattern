def _upgrade_all(self):
    if self.module.check_mode:
        self.changed = True
        self.message = 'Casks would be upgraded.'
        raise HomebrewCaskException(self.message)
    opts = [self.brew_path, 'cask', 'upgrade']
    cmd = [opt for opt in opts if opt]
    (rc, out, err) = ('', '', '')
    if self.sudo_password:
        (rc, out, err) = self._run_command_with_sudo_password(cmd)
    else:
        (rc, out, err) = self.module.run_command(cmd)
    if (rc == 0):
        if re.search('==> No Casks to upgrade', out.strip(), re.IGNORECASE):
            self.message = 'Homebrew casks already upgraded.'
        else:
            self.changed = True
            self.message = 'Homebrew casks upgraded.'
        return True
    else:
        self.failed = True
        self.message = err.strip()
        raise HomebrewCaskException(self.message)