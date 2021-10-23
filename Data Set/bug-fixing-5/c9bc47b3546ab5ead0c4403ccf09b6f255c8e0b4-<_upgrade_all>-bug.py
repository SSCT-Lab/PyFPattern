def _upgrade_all(self):
    if self.module.check_mode:
        self.changed = True
        self.message = 'Casks would be upgraded.'
        raise HomebrewCaskException(self.message)
    (rc, out, err) = self.module.run_command([self.brew_path, 'cask', 'upgrade'])
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