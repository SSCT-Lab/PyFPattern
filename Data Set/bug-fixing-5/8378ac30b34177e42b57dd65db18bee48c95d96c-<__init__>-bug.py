def __init__(self, display=None):
    self.disabled = False
    if cli:
        self._plugin_options = cli.options
    else:
        self._plugin_options = None
    super(CallbackModule, self).__init__(display=display)
    if (not HAS_PRETTYTABLE):
        self.disabled = True
        self._display.warning('The `prettytable` python module is not installed. Disabling the Slack callback plugin.')
    self.webhook_url = self._plugin_options['webook_url']
    self.channel = self._plugin_options['channel']
    self.username = self._plugin_options['username']
    self.show_invocation = (self._display.verbosity > 1)
    if (self.webhook_url is None):
        self.disabled = True
        self._display.warning('Slack Webhook URL was not provided. The Slack Webhook URL can be provided using the `SLACK_WEBHOOK_URL` environment variable.')
    else:
        self.playbook_name = None
        self.guid = uuid.uuid4().hex[:6]