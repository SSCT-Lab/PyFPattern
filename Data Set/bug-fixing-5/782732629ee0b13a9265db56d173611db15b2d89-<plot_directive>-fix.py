def plot_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    'Implementation of the ``.. plot::`` directive.\n\n    See the module docstring for details.\n    '
    return run(arguments, content, options, state_machine, state, lineno)