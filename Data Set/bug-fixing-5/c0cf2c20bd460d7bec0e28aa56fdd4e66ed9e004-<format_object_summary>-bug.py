def format_object_summary(obj, formatter: Callable, is_justify: bool=True, name: Optional[str]=None, indent_for_name: bool=True, line_break_each_value: bool=False) -> str:
    '\n    Return the formatted obj as a unicode string\n\n    Parameters\n    ----------\n    obj : object\n        must be iterable and support __getitem__\n    formatter : callable\n        string formatter for an element\n    is_justify : boolean\n        should justify the display\n    name : name, optional\n        defaults to the class name of the obj\n    indent_for_name : bool, default True\n        Whether subsequent lines should be be indented to\n        align with the name.\n    line_break_each_value : bool, default False\n        If True, inserts a line break for each value of ``obj``.\n        If False, only break lines when the a line of values gets wider\n        than the display width.\n\n        .. versionadded:: 0.25.0\n\n    Returns\n    -------\n    summary string\n\n    '
    from pandas.io.formats.console import get_console_size
    from pandas.io.formats.format import _get_adjustment
    (display_width, _) = get_console_size()
    if (display_width is None):
        display_width = (get_option('display.width') or 80)
    if (name is None):
        name = type(obj).__name__
    if indent_for_name:
        name_len = len(name)
        space1 = ('\n%s' % (' ' * (name_len + 1)))
        space2 = ('\n%s' % (' ' * (name_len + 2)))
    else:
        space1 = '\n'
        space2 = '\n '
    n = len(obj)
    if line_break_each_value:
        sep = (',\n ' + (' ' * len(name)))
    else:
        sep = ','
    max_seq_items = (get_option('display.max_seq_items') or n)
    is_truncated = (n > max_seq_items)
    adj = _get_adjustment()

    def _extend_line(s, line, value, display_width, next_line_prefix):
        if ((adj.len(line.rstrip()) + adj.len(value.rstrip())) >= display_width):
            s += line.rstrip()
            line = next_line_prefix
        line += value
        return (s, line)

    def best_len(values):
        if values:
            return max((adj.len(x) for x in values))
        else:
            return 0
    close = ', '
    if (n == 0):
        summary = '[]{}'.format(close)
    elif ((n == 1) and (not line_break_each_value)):
        first = formatter(obj[0])
        summary = '[{}]{}'.format(first, close)
    elif ((n == 2) and (not line_break_each_value)):
        first = formatter(obj[0])
        last = formatter(obj[(- 1)])
        summary = '[{}, {}]{}'.format(first, last, close)
    else:
        if (n > max_seq_items):
            n = min((max_seq_items // 2), 10)
            head = [formatter(x) for x in obj[:n]]
            tail = [formatter(x) for x in obj[(- n):]]
        else:
            head = []
            tail = [formatter(x) for x in obj]
        if is_justify:
            if line_break_each_value:
                (head, tail) = _justify(head, tail)
            elif (is_truncated or (not ((len(', '.join(head)) < display_width) and (len(', '.join(tail)) < display_width)))):
                max_length = max(best_len(head), best_len(tail))
                head = [x.rjust(max_length) for x in head]
                tail = [x.rjust(max_length) for x in tail]
        if line_break_each_value:
            max_space = (display_width - len(space2))
            value = tail[0]
            for max_items in reversed(range(1, (len(value) + 1))):
                pprinted_seq = _pprint_seq(value, max_seq_items=max_items)
                if (len(pprinted_seq) < max_space):
                    break
            head = [_pprint_seq(x, max_seq_items=max_items) for x in head]
            tail = [_pprint_seq(x, max_seq_items=max_items) for x in tail]
        summary = ''
        line = space2
        for max_items in range(len(head)):
            word = ((head[max_items] + sep) + ' ')
            (summary, line) = _extend_line(summary, line, word, display_width, space2)
        if is_truncated:
            summary += ((line.rstrip() + space2) + '...')
            line = space2
        for max_items in range((len(tail) - 1)):
            word = ((tail[max_items] + sep) + ' ')
            (summary, line) = _extend_line(summary, line, word, display_width, space2)
        (summary, line) = _extend_line(summary, line, tail[(- 1)], (display_width - 2), space2)
        summary += line
        close = (']' + close.rstrip(' '))
        summary += close
        if ((len(summary) > display_width) or line_break_each_value):
            summary += space1
        else:
            summary += ' '
        summary = ('[' + summary[len(space2):])
    return summary