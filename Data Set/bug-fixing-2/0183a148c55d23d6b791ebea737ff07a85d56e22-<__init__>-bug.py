

def __init__(self, module, user=None, cron_file=None):
    self.module = module
    self.user = user
    if (self.user is None):
        self.user = 'root'
    self.lines = None
    self.wordchars = ''.join((chr(x) for x in range(128) if (chr(x) not in ('=', "'", '"'))))
    if cron_file:
        self.cron_file = ''
        if os.path.isabs(cron_file):
            self.cron_file = cron_file
        else:
            self.cron_file = os.path.join('/etc/cron.d', cron_file)
    else:
        self.cron_file = None
    self.read()
