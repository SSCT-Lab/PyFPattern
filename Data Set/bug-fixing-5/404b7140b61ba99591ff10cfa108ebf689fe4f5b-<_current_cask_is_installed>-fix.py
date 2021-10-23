def _current_cask_is_installed(self):
    if (not self.valid_cask(self.current_cask)):
        self.failed = True
        self.message = 'Invalid cask: {0}.'.format(self.current_cask)
        raise HomebrewCaskException(self.message)
    cmd = ['{brew_path}'.format(brew_path=self.brew_path), 'cask', 'list', self.current_cask]
    (rc, out, err) = self.module.run_command(cmd)
    if (rc == 0):
        return True
    else:
        return False