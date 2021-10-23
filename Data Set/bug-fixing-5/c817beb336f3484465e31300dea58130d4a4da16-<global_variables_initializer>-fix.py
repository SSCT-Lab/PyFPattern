def global_variables_initializer():
    'Returns an Op that initializes global variables.\n\n  This is just a shortcut for `variables_initializer(global_variables())`\n\n  Returns:\n    An Op that initializes global variables in the graph.\n  '
    return variables_initializer(global_variables())