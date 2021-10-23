def _check_arguments(self, check_invalid_arguments):
    self._syslog_facility = 'LOG_USER'
    for (k, v) in list(self.params.items()):
        if ((k == '_ansible_check_mode') and v):
            self.check_mode = True
        elif (k == '_ansible_no_log'):
            self.no_log = self.boolean(v)
        elif (k == '_ansible_debug'):
            self._debug = self.boolean(v)
        elif (k == '_ansible_diff'):
            self._diff = self.boolean(v)
        elif (k == '_ansible_verbosity'):
            self._verbosity = v
        elif (k == '_ansible_selinux_special_fs'):
            self._selinux_special_fs = v
        elif (k == '_ansible_syslog_facility'):
            self._syslog_facility = v
        elif (k == '_ansible_version'):
            self.ansible_version = v
        elif (k == '_ansible_module_name'):
            self._name = v
        elif (check_invalid_arguments and (k not in self._legal_inputs)):
            self.fail_json(msg=('unsupported parameter for module: %s' % k))
        if k.startswith('_ansible_'):
            del self.params[k]
    if (self.check_mode and (not self.supports_check_mode)):
        self.exit_json(skipped=True, msg=('remote module (%s) does not support check mode' % self._name))