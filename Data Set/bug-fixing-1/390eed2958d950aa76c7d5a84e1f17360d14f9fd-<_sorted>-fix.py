

def _sorted(dict_):
    'Returns a sorted list of the dict keys, with error if keys not sortable.'
    try:
        return sorted(dict_.keys())
    except TypeError:
        raise TypeError('nest only supports dicts with sortable keys.')
