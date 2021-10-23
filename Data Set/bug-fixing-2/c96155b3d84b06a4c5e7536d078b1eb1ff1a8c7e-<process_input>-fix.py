

def process_input(self, data, input_prompt, lineno):
    '\n        Process data block for INPUT token.\n\n        '
    (decorator, input, rest) = data
    image_file = None
    image_directive = None
    is_verbatim = ((decorator == '@verbatim') or self.is_verbatim)
    is_doctest = (((decorator is not None) and decorator.startswith('@doctest')) or self.is_doctest)
    is_suppress = ((decorator == '@suppress') or self.is_suppress)
    is_okexcept = ((decorator == '@okexcept') or self.is_okexcept)
    is_okwarning = ((decorator == '@okwarning') or self.is_okwarning)
    is_savefig = ((decorator is not None) and decorator.startswith('@savefig'))
    input_lines = input.split('\n')
    if (len(input_lines) > 1):
        if (input_lines[(- 1)] != ''):
            input_lines.append('')
    continuation = ('   %s:' % ''.join((['.'] * (len(str(lineno)) + 2))))
    if is_savefig:
        (image_file, image_directive) = self.process_image(decorator)
    ret = []
    is_semicolon = False
    if (is_suppress and self.hold_count):
        store_history = False
    else:
        store_history = True
    with warnings.catch_warnings(record=True) as ws:
        if input_lines[0].endswith(';'):
            is_semicolon = True
        if is_verbatim:
            self.process_input_lines([''])
            self.IP.execution_count += 1
        else:
            self.process_input_lines(input_lines, store_history=store_history)
    if (not is_suppress):
        for (i, line) in enumerate(input_lines):
            if (i == 0):
                formatted_line = ('%s %s' % (input_prompt, line))
            else:
                formatted_line = ('%s %s' % (continuation, line))
            ret.append(formatted_line)
    if ((not is_suppress) and len(rest.strip()) and is_verbatim):
        ret.append(rest)
    self.cout.seek(0)
    processed_output = self.cout.read()
    if ((not is_suppress) and (not is_semicolon)):
        ret.append(processed_output)
    elif is_semicolon:
        ret.append('')
    filename = 'Unknown'
    lineno = 0
    if self.directive.state:
        filename = self.directive.state.document.current_source
        lineno = self.directive.state.document.current_line
    if ((not is_okexcept) and (('Traceback' in processed_output) or ('SyntaxError' in processed_output))):
        s = ('\nException in %s at block ending on line %s\n' % (filename, lineno))
        s += 'Specify :okexcept: as an option in the ipython:: block to suppress this message\n'
        sys.stdout.write(('\n\n>>>' + ('-' * 73)))
        sys.stdout.write(s)
        sys.stdout.write(processed_output)
        sys.stdout.write((('<<<' + ('-' * 73)) + '\n\n'))
        if self.warning_is_error:
            raise RuntimeError('Non Expected exception in `{}` line {}'.format(filename, lineno))
    if (not is_okwarning):
        for w in ws:
            s = ('\nWarning in %s at block ending on line %s\n' % (filename, lineno))
            s += 'Specify :okwarning: as an option in the ipython:: block to suppress this message\n'
            sys.stdout.write(('\n\n>>>' + ('-' * 73)))
            sys.stdout.write(s)
            sys.stdout.write((('-' * 76) + '\n'))
            s = warnings.formatwarning(w.message, w.category, w.filename, w.lineno, w.line)
            sys.stdout.write(s)
            sys.stdout.write((('<<<' + ('-' * 73)) + '\n'))
            if self.warning_is_error:
                raise RuntimeError('Non Expected warning in `{}` line {}'.format(filename, lineno))
    self.cout.truncate(0)
    return (ret, input_lines, processed_output, is_doctest, decorator, image_file, image_directive)
