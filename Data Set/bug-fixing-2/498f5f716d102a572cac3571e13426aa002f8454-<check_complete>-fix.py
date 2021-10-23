

def check_complete(self, cell: str):
    "Return whether a block of code is ready to execute, or should be continued\n\n        Parameters\n        ----------\n        source : string\n          Python input code, which can be multiline.\n\n        Returns\n        -------\n        status : str\n          One of 'complete', 'incomplete', or 'invalid' if source is not a\n          prefix of valid code.\n        indent_spaces : int or None\n          The number of spaces by which to indent the next line of code. If\n          status is not 'incomplete', this is None.\n        "
    cell += '\n'
    lines = cell.splitlines(keepends=True)
    if lines[(- 1)][:(- 1)].endswith('\\'):
        return ('incomplete', find_last_indent(lines))
    try:
        for transform in self.cleanup_transforms:
            lines = transform(lines)
    except SyntaxError:
        return ('invalid', None)
    if lines[0].startswith('%%'):
        if lines[(- 1)].strip():
            return ('incomplete', find_last_indent(lines))
        else:
            return ('complete', None)
    try:
        for transform in self.line_transforms:
            lines = transform(lines)
        lines = self.do_token_transforms(lines)
    except SyntaxError:
        return ('invalid', None)
    tokens_by_line = make_tokens_by_line(lines)
    if (not tokens_by_line):
        return ('incomplete', find_last_indent(lines))
    if (tokens_by_line[(- 1)][(- 1)].type != tokenize.ENDMARKER):
        return ('incomplete', find_last_indent(lines))
    if (len(tokens_by_line) == 1):
        return ('incomplete', find_last_indent(lines))
    toks_last_line = tokens_by_line[(- 2)]
    ix = (len(toks_last_line) - 1)
    while ((ix >= 0) and (toks_last_line[ix].type in {tokenize.NEWLINE, tokenize.COMMENT})):
        ix -= 1
    if (toks_last_line[ix].string == ':'):
        ix = 0
        while (toks_last_line[ix].type in {tokenize.INDENT, tokenize.DEDENT}):
            ix += 1
        indent = toks_last_line[ix].start[1]
        return ('incomplete', (indent + 4))
    if (not lines[(- 1)].strip()):
        return ('complete', None)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', SyntaxWarning)
            compile_command(''.join(lines), symbol='exec')
    except (SyntaxError, OverflowError, ValueError, TypeError, MemoryError, SyntaxWarning):
        return ('invalid', None)
    else:
        if ((len(lines) > 1) and (not lines[(- 1)].strip().endswith(':')) and (not lines[(- 2)][:(- 1)].endswith('\\'))):
            return ('incomplete', find_last_indent(lines))
    return ('complete', None)
