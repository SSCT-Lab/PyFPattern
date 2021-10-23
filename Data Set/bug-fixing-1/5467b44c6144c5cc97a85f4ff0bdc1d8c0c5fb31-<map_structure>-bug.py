

def map_structure(func, *structure, **check_types_dict):
    'Applies `func` to each entry in `structure` and returns a new structure.\n\n  Applies `func(x[0], x[1], ...)` where x[i] is an entry in\n  `structure[i]`.  All structures in `structure` must have the same arity,\n  and the return value will contain the results in the same structure.\n\n  Args:\n    func: A callable that acceps as many arguments are there are structures.\n    *structure: scalar, or tuple or list of constructed scalars and/or other\n      tuples/lists, or scalars.  Note: numpy arrays are considered scalars.\n    **check_types_dict: only valid keyword argument is `check_types`. If set to\n      `True` (default) the types of iterables within the  structures have to be\n      same (e.g. `map_structure(func, [1], (1,))` raises a `TypeError`\n      exception). To allow this set this argument to `False`.\n\n  Returns:\n    A new structure with the same arity as `structure`, whose values correspond\n    to `func(x[0], x[1], ...)` where `x[i]` is a value in the corresponding\n    location in `structure[i]`. If there are different sequence types and\n    `check_types` is `False` the sequence types of the first structure will be\n    used.\n\n  Raises:\n    TypeError: If `func` is not callable or if the structures do not match\n      each other by depth tree.\n    ValueError: If no structure is provided or if the structures do not match\n      each other by type.\n    ValueError: If wrong keyword arguments are provided.\n  '
    if (not callable(func)):
        raise TypeError(('func must be callable, got: %s' % func))
    if (not structure):
        raise ValueError('Must provide at least one structure')
    if check_types_dict:
        if (('check_types' not in check_types_dict) or (len(check_types_dict) > 1)):
            raise ValueError('Only valid keyword argument is check_types')
        check_types = check_types_dict['check_types']
    else:
        check_types = True
    for other in structure[1:]:
        assert_same_structure(structure[0], other, check_types=check_types)
    flat_structure = [flatten(s) for s in structure]
    entries = zip(*flat_structure)
    return pack_sequence_as(structure[0], [func(*x) for x in entries])
