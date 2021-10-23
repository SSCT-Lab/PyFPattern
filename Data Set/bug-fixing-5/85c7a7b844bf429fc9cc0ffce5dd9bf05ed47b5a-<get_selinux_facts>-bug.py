def get_selinux_facts(self):
    if (not HAVE_SELINUX):
        self.facts['selinux'] = False
        return
    self.facts['selinux'] = {
        
    }
    if (not selinux.is_selinux_enabled()):
        self.facts['selinux']['status'] = 'disabled'
    else:
        self.facts['selinux']['status'] = 'enabled'
        try:
            self.facts['selinux']['policyvers'] = selinux.security_policyvers()
        except (AttributeError, OSError):
            self.facts['selinux']['policyvers'] = 'unknown'
        try:
            (rc, configmode) = selinux.selinux_getenforcemode()
            if (rc == 0):
                self.facts['selinux']['config_mode'] = Facts.SELINUX_MODE_DICT.get(configmode, 'unknown')
            else:
                self.facts['selinux']['config_mode'] = 'unknown'
        except (AttributeError, OSError):
            self.facts['selinux']['config_mode'] = 'unknown'
        try:
            mode = selinux.security_getenforce()
            self.facts['selinux']['mode'] = Facts.SELINUX_MODE_DICT.get(mode, 'unknown')
        except (AttributeError, OSError):
            self.facts['selinux']['mode'] = 'unknown'
        try:
            (rc, policytype) = selinux.selinux_getpolicytype()
            if (rc == 0):
                self.facts['selinux']['type'] = policytype
            else:
                self.facts['selinux']['type'] = 'unknown'
        except (AttributeError, OSError):
            self.facts['selinux']['type'] = 'unknown'