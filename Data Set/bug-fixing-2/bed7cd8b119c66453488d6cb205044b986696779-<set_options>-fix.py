

def set_options(self, options):
    '\n        Configures this connection information instance with data from\n        options specified by the user on the command line. These have a\n        lower precedence than those set on the play or host.\n        '
    self.become = options.become
    self.become_method = options.become_method
    self.become_user = options.become_user
    self.check_mode = boolean(options.check, strict=False)
    self.diff = boolean(options.diff, strict=False)
    for flag in OPTION_FLAGS:
        attribute = getattr(options, flag, False)
        if attribute:
            setattr(self, flag, attribute)
    if (hasattr(options, 'timeout') and options.timeout):
        self.timeout = int(options.timeout)
    if hasattr(options, 'tags'):
        self.only_tags.update(options.tags)
    if (len(self.only_tags) == 0):
        self.only_tags = set(['all'])
    if hasattr(options, 'skip_tags'):
        self.skip_tags.update(options.skip_tags)
