def v2_runner_on_skipped(self, result, **kwargs):
    'Run when a task is skipped.'
    if (self._display.verbosity > 1):
        self._print_task()
        self.last_skipped = False
        line_length = 120
        spaces = (' ' * ((31 - len(result._host.name)) - 4))
        line = '  * {}{}- {}'.format(colorize(result._host.name, 'not_so_bold'), spaces, colorize('skipped', 'skipped'))
        reason = (result._result.get('skipped_reason', '') or result._result.get('skip_reason', ''))
        if (len(reason) < 50):
            line += ' -- {}'.format(reason)
            print('{} {}---------'.format(line, ('-' * (line_length - len(line)))))
        else:
            print('{} {}'.format(line, ('-' * (line_length - len(line)))))
            print(self._indent_text(reason, 8))
            print(reason)