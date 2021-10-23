def process_function_docstring(docstring):
    docstring = re.sub('\\n    # (.*)\\n', '\\n    __\\1__\\n\\n', docstring)
    docstring = re.sub('\\n        # (.*)\\n', '\\n        __\\1__\\n\\n', docstring)
    docstring = re.sub('    ([^\\s\\\\\\(]+):(.*)\\n', '    - __\\1__:\\2\\n', docstring)
    docstring = docstring.replace(('    ' * 6), '\t\t')
    docstring = docstring.replace(('    ' * 4), '\t')
    docstring = docstring.replace('    ', '')
    return docstring