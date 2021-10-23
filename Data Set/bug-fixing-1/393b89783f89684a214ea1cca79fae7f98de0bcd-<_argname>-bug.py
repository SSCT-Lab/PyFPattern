

def _argname(in_types, names):
    'Assigns user friendly names for the input types.\n\n    This function also asserts that lenghts of in_types and names are the\n    same.\n\n    Args:\n        in_types (tuple of TypeInfoTuple): Tuple of type information to assign\n            name to.\n        names (tuple of str): Human-readabel names of ``in_types``.\n    '
    if (len(in_types) != len(names)):
        raise InvalidType('{} argument(s)'.format(str(len(names))), '{} argument(s)'.format(str(len(in_types))), 'Invalid number of arguments')
    for (in_type, name) in zip(in_types, names):
        if isinstance(in_type, Variable):
            in_type.name = name
