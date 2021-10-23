def _print_host_or_item(self, host_or_item, changed, msg, diff, is_host, error, stdout, stderr):
    if is_host:
        indent_level = 0
        name = colorize(host_or_item.name, 'not_so_bold')
    else:
        indent_level = 4
        if isinstance(host_or_item, dict):
            if ('key' in host_or_item.keys()):
                host_or_item = host_or_item['key']
        name = colorize(to_text(host_or_item), 'bold')
    if error:
        color = 'failed'
        change_string = colorize('FAILED!!!', color)
    else:
        color = ('changed' if changed else 'ok')
        change_string = colorize('changed={}'.format(changed), color)
    msg = colorize(msg, color)
    line_length = 120
    spaces = (' ' * ((40 - len(name)) - indent_level))
    line = '{}  * {}{}- {}'.format((' ' * indent_level), name, spaces, change_string)
    if (len(msg) < 50):
        line += ' -- {}'.format(msg)
        print('{} {}---------'.format(line, ('-' * (line_length - len(line)))))
    else:
        print('{} {}'.format(line, ('-' * (line_length - len(line)))))
        print(self._indent_text(msg, (indent_level + 4)))
    if diff:
        self._print_diff(diff, indent_level)
    if stdout:
        stdout = colorize(stdout, 'failed')
        print(self._indent_text(stdout, (indent_level + 4)))
    if stderr:
        stderr = colorize(stderr, 'failed')
        print(self._indent_text(stderr, (indent_level + 4)))