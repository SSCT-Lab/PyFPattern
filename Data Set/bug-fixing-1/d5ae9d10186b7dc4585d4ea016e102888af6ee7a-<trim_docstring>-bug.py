

def trim_docstring(docstring):
    if (not docstring):
        return ''
    lines = docstring.expandtabs().splitlines()
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, (len(line) - len(stripped)))
    trimmed = [lines[0].strip()]
    if (indent < sys.maxint):
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    while (trimmed and (not trimmed[(- 1)])):
        trimmed.pop()
    while (trimmed and (not trimmed[0])):
        trimmed.pop(0)
    return '\n'.join(trimmed)
