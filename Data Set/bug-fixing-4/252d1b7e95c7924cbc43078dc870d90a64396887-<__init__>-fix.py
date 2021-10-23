def __init__(self, *args, **kwargs):
    'init.'
    super(Connection, self).__init__(*args, **kwargs)
    if (hasattr(self, '_shell') and (self._shell.SHELL_FAMILY == 'powershell')):
        self.module_implementation_preferences = ('.ps1', '.exe', '')
        self.become_methods = ['runas']
        self.allow_executable = False
        self.has_pipelining = False
        self.allow_extras = True