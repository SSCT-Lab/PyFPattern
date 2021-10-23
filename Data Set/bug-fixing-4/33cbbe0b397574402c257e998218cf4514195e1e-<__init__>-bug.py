def __init__(self, module, path=path, casks=None, state=None, update_homebrew=False, install_options=None):
    if (not install_options):
        install_options = list()
    self._setup_status_vars()
    self._setup_instance_vars(module=module, path=path, casks=casks, state=state, update_homebrew=update_homebrew, install_options=install_options)
    self._prep()