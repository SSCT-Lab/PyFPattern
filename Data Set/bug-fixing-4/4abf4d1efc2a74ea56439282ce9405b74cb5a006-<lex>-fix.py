def lex(s, name=None, trim_whitespace=True, line_offset=0, delimiters=None):
    if (delimiters is None):
        delimiters = (Template.default_namespace['start_braces'], Template.default_namespace['end_braces'])
    in_expr = False
    chunks = []
    last = 0
    last_pos = ((line_offset + 1), 1)
    token_re = re.compile(('%s|%s' % (re.escape(delimiters[0]), re.escape(delimiters[1]))))
    for match in token_re.finditer(s):
        expr = match.group(0)
        pos = find_position(s, match.end(), last, last_pos)
        if ((expr == delimiters[0]) and in_expr):
            raise TemplateError(('%s inside expression' % delimiters[0]), position=pos, name=name)
        elif ((expr == delimiters[1]) and (not in_expr)):
            raise TemplateError(('%s outside expression' % delimiters[1]), position=pos, name=name)
        if (expr == delimiters[0]):
            part = s[last:match.start()]
            if part:
                chunks.append(part)
            in_expr = True
        else:
            chunks.append((s[last:match.start()], last_pos))
            in_expr = False
        last = match.end()
        last_pos = pos
    if in_expr:
        raise TemplateError(('No %s to finish last expression' % delimiters[1]), name=name, position=last_pos)
    part = s[last:]
    if part:
        chunks.append(part)
    if trim_whitespace:
        chunks = trim_lex(chunks)
    return chunks