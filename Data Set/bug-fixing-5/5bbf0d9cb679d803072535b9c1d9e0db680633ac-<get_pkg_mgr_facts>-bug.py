def get_pkg_mgr_facts(self):
    if (self.facts['system'] == 'OpenBSD'):
        self.facts['pkg_mgr'] = 'openbsd_pkg'
    else:
        self.facts['pkg_mgr'] = 'unknown'
        for pkg in Facts.PKG_MGRS:
            if os.path.exists(pkg['path']):
                self.facts['pkg_mgr'] = pkg['name']