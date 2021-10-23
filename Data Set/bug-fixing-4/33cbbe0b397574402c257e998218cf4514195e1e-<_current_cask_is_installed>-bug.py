def _current_cask_is_installed(self):
    if (not self.valid_cask(self.current_cask)):
        self.failed = True
        self.message = 'Invalid cask: {0}.'.format(self.current_cask)
        raise HomebrewCaskException(self.message)
    cmd = ['{brew_path}'.format(brew_path=self.brew_path), 'cask', 'list']
    (rc, out, err) = self.module.run_command(cmd)
    if ('nothing to list' in err):
        return False
    elif (rc == 0):
        casks = [cask_.strip() for cask_ in out.split('\n') if cask_.strip()]
        return (self.current_cask in casks)
    else:
        self.failed = True
        self.message = err.strip()
        raise HomebrewCaskException(self.message)