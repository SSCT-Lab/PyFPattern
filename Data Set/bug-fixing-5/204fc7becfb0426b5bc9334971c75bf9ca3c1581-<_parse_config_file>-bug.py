def _parse_config_file(self, cfile=None):
    ' return flat configuration settings from file(s) '
    if (cfile is None):
        cfile = self._config_file
    ftype = get_config_type(cfile)
    if (cfile is not None):
        if (ftype == 'ini'):
            self._parsers[cfile] = configparser.ConfigParser()
            try:
                self._parsers[cfile].read(cfile)
            except configparser.Error as e:
                raise AnsibleOptionsError(('Error reading config file (%s): %s' % (cfile, to_native(e))))
        else:
            raise AnsibleOptionsError(('Unsupported configuration file type: %s' % to_native(ftype)))