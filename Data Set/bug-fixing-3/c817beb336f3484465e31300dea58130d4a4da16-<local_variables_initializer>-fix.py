def local_variables_initializer():
    'Returns an Op that initializes all local variables.\n\n  This is just a shortcut for `variables_initializer(local_variables())`\n\n  Returns:\n    An Op that initializes all local variables in the graph.\n  '
    return variables_initializer(local_variables())