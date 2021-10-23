def update_config_data(self, defs=None, configfile=None):
    ' really: update constants '
    if (defs is None):
        defs = self._base_defs
    if (configfile is None):
        configfile = self._config_file
    if (not isinstance(defs, dict)):
        raise AnsibleOptionsError(('Invalid configuration definition type: %s for %s' % (type(defs), defs)))
    self.data.update_setting(Setting('CONFIG_FILE', configfile, ''))
    origin = None
    for config in defs:
        if (not isinstance(defs[config], dict)):
            raise AnsibleOptionsError(("Invalid configuration definition '%s': type is %s" % (to_native(config), type(defs[config]))))
        (value, origin) = self.get_config_value_and_origin(config, configfile)
        self.data.update_setting(Setting(config, value, origin))
    if self.UNABLE:
        sys.stderr.write(('Unable to set correct type for:\n\t%s\n' % '\n\t'.join(self.UNABLE)))
    if self.DEPRECATED:
        for (k, reason) in self.DEPRECATED:
            sys.stderr.write('[DEPRECATED] %s: %(why)s. It will be removed in %(version)s. As alternative %(alternative)s', (k, reason))