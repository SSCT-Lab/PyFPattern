def _leading_trailing(a, index=()):
    '\n    Keep only the N-D corners (leading and trailing edges) of an array.\n\n    Should be passed a base-class ndarray, since it makes no guarantees about\n    preserving subclasses.\n    '
    edgeitems = _format_options['edgeitems']
    axis = len(index)
    if (axis == a.ndim):
        return a[index]
    if (a.shape[axis] > (2 * edgeitems)):
        return concatenate((_leading_trailing(a, (index + np.index_exp[:edgeitems])), _leading_trailing(a, (index + np.index_exp[(- edgeitems):]))), axis=axis)
    else:
        return _leading_trailing(a, (index + np.index_exp[:]))