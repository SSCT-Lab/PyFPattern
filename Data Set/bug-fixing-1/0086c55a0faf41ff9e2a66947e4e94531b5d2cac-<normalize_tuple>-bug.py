

def normalize_tuple(value, n, name):
    'Transforms a single integer or iterable of integers into an integer tuple.\n\n  Arguments:\n    value: The value to validate and convert. Could an int, or any iterable\n      of ints.\n    n: The size of the tuple to be returned.\n    name: The name of the argument being validated, e.g. "strides" or\n      "kernel_size". This is only used to format error messages.\n\n  Returns:\n    A tuple of n integers.\n\n  Raises:\n    ValueError: If something else than an int/long or iterable thereof was\n      passed.\n  '
    if isinstance(value, int):
        return ((value,) * n)
    else:
        try:
            value_tuple = tuple(value)
        except TypeError:
            raise ValueError(((((('The `' + name) + '` argument must be a tuple of ') + str(n)) + ' integers. Received: ') + str(value)))
        if (len(value_tuple) != n):
            raise ValueError(((((('The `' + name) + '` argument must be a tuple of ') + str(n)) + ' integers. Received: ') + str(value)))
        for single_value in value_tuple:
            try:
                int(single_value)
            except ValueError:
                raise ValueError((((((((((('The `' + name) + '` argument must be a tuple of ') + str(n)) + ' integers. Received: ') + str(value)) + ' including element ') + str(single_value)) + ' of type') + ' ') + str(type(single_value))))
        return value_tuple
