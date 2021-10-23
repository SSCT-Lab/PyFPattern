def diff_config(self, session):
    commands = [('configure session %s' % session), 'show session-config diffs', 'end']
    if isinstance(self, Eapi):
        response = self.execute(commands, output='text')
    else:
        response = self.execute(commands)
    return response[(- 2)]