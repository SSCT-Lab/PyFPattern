def _check_known_errors(self, responses):
    for resp in responses:
        if ('usage: tmsh' in resp):
            raise F5ModuleError("tmsh command printed its 'help' message instead of running your command. This usually indicates unbalanced quotes.")