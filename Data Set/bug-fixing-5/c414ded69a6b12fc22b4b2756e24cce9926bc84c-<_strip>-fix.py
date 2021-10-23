def _strip(self, data):
    for regex in self._terminal.ansi_re:
        data = regex.sub('', data)
    return data