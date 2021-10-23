def render_function(function, method=True):
    subblocks = []
    signature = get_function_signature(function, method=method)
    signature = signature.replace((function.__module__ + '.'), '')
    subblocks.append((('### ' + function.__name__) + '\n'))
    subblocks.append(code_snippet(signature))
    docstring = function.__doc__
    if docstring:
        subblocks.append(process_docstring(docstring))
    return '\n\n'.join(subblocks)