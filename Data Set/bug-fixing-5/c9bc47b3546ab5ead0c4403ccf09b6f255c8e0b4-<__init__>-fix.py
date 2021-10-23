def __init__(self, module, path=path, casks=None, state=None, sudo_password=None, update_homebrew=False, install_options=None, accept_external_apps=False, upgrade_all=False, greedy=False):
    if (not install_options):
        install_options = list()
    self._setup_status_vars()
    self._setup_instance_vars(module=module, path=path, casks=casks, state=state, sudo_password=sudo_password, update_homebrew=update_homebrew, install_options=install_options, accept_external_apps=accept_external_apps, upgrade_all=upgrade_all, greedy=greedy)
    self._prep()