def __init__(self, display=None):
    super(CallbackModule, self).__init__(display=display)
    self._options = cli.options
    if (not HAS_PRETTYTABLE):
        self.disabled = True
        self._display.warning('The `prettytable` python module is not installed. Disabling the Slack callback plugin.')
    self.playbook_name = None
    self.guid = uuid.uuid4().hex[:6]