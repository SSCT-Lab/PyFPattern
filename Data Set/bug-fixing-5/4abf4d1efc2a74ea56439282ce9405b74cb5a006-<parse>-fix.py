def parse(s, name=None, line_offset=0, delimiters=None):
    if (delimiters is None):
        delimiters = (Template.default_namespace['start_braces'], Template.default_namespace['end_braces'])
    tokens = lex(s, name=name, line_offset=line_offset, delimiters=delimiters)
    result = []
    while tokens:
        (next_chunk, tokens) = parse_expr(tokens, name)
        result.append(next_chunk)
    return result