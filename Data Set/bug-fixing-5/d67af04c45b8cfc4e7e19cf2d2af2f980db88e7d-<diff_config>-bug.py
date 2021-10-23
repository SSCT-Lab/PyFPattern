def diff_config(self, session):
    commands = [('configure session %s' % session), 'show session-config diffs', 'end']
    response = self.execute(commands)
    return response[(- 2)]