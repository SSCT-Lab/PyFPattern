def execute(self, commands, output='json', **kwargs):
    'Send commands to the device.\n        '
    if (self.url is None):
        raise NetworkError('Not connected to endpoint.')
    if (self.enable is not None):
        commands.insert(0, self.enable)