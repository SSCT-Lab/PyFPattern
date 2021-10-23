def _parse_config_file(self, cfile=None):
    ' return flat configuration settings from file(s) '
    if (cfile is None):
        cfile = self._config_file
    ftype = get_config_type(cfile)
    if (cfile is not None):
        if (ftype == 'ini'):
            self._parsers[cfile] = configparser.ConfigParser()
            with open(cfile, 'rb') as f:
                try:
                    cfg_text = to_text(f.read(), errors='surrogate_or_strict')
                except UnicodeError:
                    raise AnsibleOptionsError(('Error reading config file(%s) because the config file was not utf8 encoded: %s' % (cfile, to_native(e))))
            try:
                if PY3:
                    self._parsers[cfile].read_string(cfg_text)
                else:
                    cfg_file = io.StringIO(cfg_text)
                    self._parsers[cfile].readfp(cfg_file)
            except configparser.Error as e:
                raise AnsibleOptionsError(('Error reading config file (%s): %s' % (cfile, to_native(e))))
        else:
            raise AnsibleOptionsError(('Unsupported configuration file type: %s' % to_native(ftype)))