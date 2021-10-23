def __init__(self):
    super(CallbackModule, self).__init__()
    if (not HAS_PRETTYTABLE):
        self.disabled = True
        self.display.warning('The `prettytable` python module is not installed. Disabling the HipChat callback plugin.')
    self.msg_uri = 'https://api.hipchat.com/v1/rooms/message'
    self.token = os.getenv('HIPCHAT_TOKEN')
    self.room = os.getenv('HIPCHAT_ROOM', 'ansible')
    self.from_name = os.getenv('HIPCHAT_FROM', 'ansible')
    self.allow_notify = (os.getenv('HIPCHAT_NOTIFY') != 'false')
    if (self.token is None):
        self.disabled = True
        self.display.warning('HipChat token could not be loaded. The HipChat token can be provided using the `HIPCHAT_TOKEN` environment variable.')
    self.printed_playbook = False
    self.playbook_name = None
    self.play = None