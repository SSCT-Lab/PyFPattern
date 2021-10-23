

def _uninstall_current_package(self):
    if (not self.valid_package(self.current_package)):
        self.failed = True
        self.message = 'Invalid package: {0}.'.format(self.current_package)
        raise HomebrewException(self.message)
    if (not self._current_package_is_installed()):
        self.unchanged_count += 1
        self.message = 'Package already uninstalled: {0}'.format(self.current_package)
        return True
    if self.module.check_mode:
        self.changed = True
        self.message = 'Package would be uninstalled: {0}'.format(self.current_package)
        raise HomebrewException(self.message)
    opts = (([self.brew_path, 'uninstall', '--force'] + self.install_options) + [self.current_package])
    cmd = [opt for opt in opts if opt]
    (rc, out, err) = self.module.run_command(cmd)
    if (not self._current_package_is_installed()):
        self.changed_count += 1
        self.changed = True
        self.message = 'Package uninstalled: {0}'.format(self.current_package)
        return True
    else:
        self.failed = True
        self.message = err.strip()
        raise HomebrewException(self.message)
