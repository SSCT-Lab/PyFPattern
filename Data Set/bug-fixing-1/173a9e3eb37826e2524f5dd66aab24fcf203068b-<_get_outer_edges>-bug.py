

def _get_outer_edges(a, range):
    '\n    Determine the outer bin edges to use, from either the data or the range\n    argument\n    '
    if (range is not None):
        (first_edge, last_edge) = range
    elif (a.size == 0):
        (first_edge, last_edge) = (0, 1)
    else:
        (first_edge, last_edge) = (a.min(), a.max())
    if (first_edge > last_edge):
        raise ValueError('max must be larger than min in range parameter.')
    if (not (np.isfinite(first_edge) and np.isfinite(last_edge))):
        raise ValueError('range parameter must be finite.')
    if (first_edge == last_edge):
        first_edge = (first_edge - 0.5)
        last_edge = (last_edge + 0.5)
    return (first_edge, last_edge)
