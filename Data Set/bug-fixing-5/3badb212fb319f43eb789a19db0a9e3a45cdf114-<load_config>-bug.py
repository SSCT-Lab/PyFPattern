def load_config(self, config, commit=False, replace=False):
    ' Loads the configuration into the remote device\n        '
    session = ('ansible_%s' % int(time.time()))
    commands = [('configure session %s' % session)]
    if replace:
        commands.append('rollback clean-config')
    commands.extend(config)
    if (commands[(- 1)] != 'end'):
        commands.append('end')
    try:
        self.execute(commands)
        diff = self.diff_config(session)
        if commit:
            self.commit_config(session)
        else:
            self.execute([('no configure session %s' % session)])
    except NetworkError:
        exc = get_exception()
        if ('timeout trying to send command' in exc.message):
            if isinstance(self, Cli):
                self.execute(['\x03', 'end'])
        self.abort_config(session)
        diff = None
        raise
    return diff