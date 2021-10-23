def is_instance_factory(_type):
    '\n\n    Parameters\n    ----------\n    `_type` - the type to be checked against\n\n    Returns\n    -------\n    validator - a function of a single argument x , which returns the\n                True if x is an instance of `_type`\n\n    '
    if isinstance(_type, (tuple, list)):
        _type = tuple(_type)
        from pandas.formats.printing import pprint_thing
        type_repr = '|'.join(map(pprint_thing, _type))
    else:
        type_repr = ("'%s'" % _type)

    def inner(x):
        if (not isinstance(x, _type)):
            raise ValueError(('Value must be an instance of %s' % type_repr))
    return inner