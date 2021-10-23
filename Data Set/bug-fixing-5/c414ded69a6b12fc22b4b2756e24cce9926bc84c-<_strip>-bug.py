def _strip(self, data):
    'Removes ANSI codes from device response'
    for regex in self._terminal.ansi_re:
        data = regex.sub('', data)
    return data