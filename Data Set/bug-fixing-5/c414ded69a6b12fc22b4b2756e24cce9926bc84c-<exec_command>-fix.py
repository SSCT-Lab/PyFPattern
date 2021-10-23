def exec_command(self, cmd):
    " {'command': <str>, 'prompt': <str>, 'answer': <str>} "
    try:
        obj = json.loads(cmd)
    except ValueError:
        obj = {
            'command': str(cmd).strip(),
        }
    if (obj['command'] == 'close_shell()'):
        return self.close_shell()
    elif (obj['command'] == 'prompt()'):
        return (0, self._matched_prompt, '')
    elif (obj['command'] == 'history()'):
        return (0, self._history, '')
    try:
        if (self._shell is None):
            self.open_shell()
    except AnsibleConnectionFailure as exc:
        return (1, '', str(exc))
    try:
        out = self.send(obj)
        return (0, out, '')
    except (AnsibleConnectionFailure, ValueError) as exc:
        return (1, '', str(exc))