def load_config(self, config, session, commit=False, replace=False, **kwargs):
    ' Loads the configuration into the remote device\n\n        This method handles the actual loading of the config\n        commands into the remote EOS device.  By default the\n        config specified is merged with the current running-config.\n\n        :param config: ordered list of config commands to load\n        :param replace: replace current config when True otherwise merge\n\n        :returns list: ordered set of responses from device\n        '
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
    except NetworkError:
        self.abort_config(session)
        diff = None
        raise
    return diff