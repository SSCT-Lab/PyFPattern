def get_module_docstring(filepath):
    'Extract the module docstring.\n\n    Also finds the line at which the docstring ends.\n    '
    co = compile(open(filepath, encoding='utf-8').read(), filepath, 'exec')
    if (co.co_consts and isinstance(co.co_consts[0], six.string_types)):
        docstring = co.co_consts[0]
    else:
        print(('Could not get the docstring from ' + filepath))
        docstring = ''
    return (docstring, co.co_firstlineno)