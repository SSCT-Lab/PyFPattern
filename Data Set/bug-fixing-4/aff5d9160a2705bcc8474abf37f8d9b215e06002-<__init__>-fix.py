def __init__(self):
    self._display = display
    if HAS_OD:
        self.disabled = False
        self.super_ref = super(CallbackModule, self)
        self.super_ref.__init__()
        self.removed_attributes = ('delta', 'end', 'failed', 'failed_when_result', 'invocation', 'start', 'stdout_lines')
        self.hosts = OrderedDict()
        self.keep = False
        self.shown_title = False
        self.count = dict(play=0, handler=0, task=0)
        self.type = 'foo'
        sys.stdout.write(((vt100.reset + vt100.save) + vt100.clearline))
        sys.stdout.flush()
    else:
        display.warning("The 'dense' callback plugin requires OrderedDict which is not available in this version of python, disabling.")
        self.disabled = True