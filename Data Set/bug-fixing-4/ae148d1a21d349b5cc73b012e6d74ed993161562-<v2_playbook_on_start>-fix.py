def v2_playbook_on_start(self, playbook):
    if (self._display.verbosity > 1):
        from os.path import basename
        self._display.banner(('PLAYBOOK: %s' % basename(playbook._file_name)))
    if (self._display.verbosity > 3):
        if (self._options is not None):
            for option in dir(self._options):
                if (option.startswith('_') or (option in ['read_file', 'ensure_value', 'read_module'])):
                    continue
                val = getattr(self._options, option)
                if (val and (self._display.verbosity > 3)):
                    self._display.display(('%s: %s' % (option, val)), color=C.COLOR_VERBOSE, screen_only=True)