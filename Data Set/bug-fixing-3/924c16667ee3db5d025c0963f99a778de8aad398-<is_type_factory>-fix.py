def is_type_factory(_type):
    '\n\n    Parameters\n    ----------\n    `_type` - a type to be compared against (e.g. type(x) == `_type`)\n\n    Returns\n    -------\n    validator - a function of a single argument x , which raises\n                ValueError if type(x) is not equal to `_type`\n\n    '

    def inner(x):
        if (type(x) != _type):
            raise ValueError(("Value must have type '%s'" % str(_type)))
    return inner