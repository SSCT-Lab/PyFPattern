def process_class_docstring(docstring):
    docstring = re.sub('\\n    # (.*)\\n', '\\n    __\\1__\\n\\n', docstring)
    docstring = re.sub('    ([^\\s\\\\]+):(.*)\\n', '    - __\\1__:\\2\\n', docstring)
    docstring = docstring.replace(('    ' * 5), '\t\t')
    docstring = docstring.replace(('    ' * 3), '\t')
    docstring = docstring.replace('    ', '')
    return docstring