

def dict_merge(base, other):
    ' Return a new dict object that combines base and other\n\n    This will create a new dict object that is a combination of the key/value\n    pairs from base and other.  When both keys exist, the value will be\n    selected from other.  If the value is a list object, the two lists will\n    be combined and duplicate entries removed.\n\n    :param base: dict object to serve as base\n    :param other: dict object to combine with base\n\n    :returns: new combined dict object\n    '
    if (not isinstance(base, dict)):
        raise AssertionError('`base` must be of type <dict>')
    if (not isinstance(other, dict)):
        raise AssertionError('`other` must be of type <dict>')
    combined = dict()
    for (key, value) in iteritems(base):
        if isinstance(value, dict):
            if (key in other):
                item = other.get(key)
                if (item is not None):
                    combined[key] = dict_merge(value, other[key])
                else:
                    combined[key] = item
            else:
                combined[key] = value
        elif isinstance(value, list):
            if (key in other):
                item = other.get(key)
                if (item is not None):
                    try:
                        combined[key] = list(set(chain(value, item)))
                    except TypeError:
                        value.extend([i for i in item if (i not in value)])
                        combined[key] = value
                else:
                    combined[key] = item
            else:
                combined[key] = value
        elif (key in other):
            other_value = other.get(key)
            if (other_value is not None):
                if (sort_list(base[key]) != sort_list(other_value)):
                    combined[key] = other_value
                else:
                    combined[key] = value
            else:
                combined[key] = other_value
        else:
            combined[key] = value
    for key in set(other.keys()).difference(base.keys()):
        combined[key] = other.get(key)
    return combined
