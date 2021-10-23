def _check_known_errors(self, responses):
    pattern = '^[0-9A-Fa-f]+:?\\d+?:'
    for resp in responses:
        if ('usage: tmsh' in resp):
            raise F5ModuleError("tmsh command printed its 'help' message instead of running your command. This usually indicates unbalanced quotes.")
        if re.match(pattern, resp):
            raise F5ModuleError(str(resp))