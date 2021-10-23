def __init__(self, display=None, options=None):
    if display:
        self._display = display
    else:
        self._display = global_display
    if cli:
        self._options = cli.options
    else:
        self._options = None
    if (self._display.verbosity >= 4):
        name = getattr(self, 'CALLBACK_NAME', 'unnamed')
        ctype = getattr(self, 'CALLBACK_TYPE', 'old')
        version = getattr(self, 'CALLBACK_VERSION', '1.0')
        self._display.vvvv(('Loading callback plugin %s of type %s, v%s from %s' % (name, ctype, version, sys.modules[self.__module__].__file__)))
    self.disabled = False
    self._plugin_options = {
        
    }
    if (options is not None):
        self.set_options(options)
    self._hide_in_debug = ('changed', 'failed', 'item', 'skipped', 'invocation')