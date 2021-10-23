def plot_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    return run(arguments, content, options, state_machine, state, lineno)