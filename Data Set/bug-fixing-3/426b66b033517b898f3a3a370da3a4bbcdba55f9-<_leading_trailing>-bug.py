def _leading_trailing(a):
    edgeitems = _format_options['edgeitems']
    if (a.ndim == 1):
        if (len(a) > (2 * edgeitems)):
            b = concatenate((a[:edgeitems], a[(- edgeitems):]))
        else:
            b = a
    else:
        if (len(a) > (2 * edgeitems)):
            l = [_leading_trailing(a[i]) for i in range(min(len(a), edgeitems))]
            l.extend([_leading_trailing(a[(- i)]) for i in range(min(len(a), edgeitems), 0, (- 1))])
        else:
            l = [_leading_trailing(a[i]) for i in range(0, len(a))]
        b = concatenate(tuple(l))
    return b