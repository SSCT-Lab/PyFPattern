

@staticmethod
def _convert_dx(dx, x0, xconv, convert):
    '\n        Small helper to do logic of width conversion flexibly.\n\n        *dx* and *x0* have units, but *xconv* has already been converted\n        to unitless (and is an ndarray).  This allows the *dx* to have units\n        that are different from *x0*, but are still accepted by the\n        ``__add__`` operator of *x0*.\n        '
    assert (type(xconv) is np.ndarray)
    if (xconv.size == 0):
        return convert(dx)
    try:
        try:
            x0 = x0[0]
        except (TypeError, IndexError, KeyError):
            x0 = x0
        try:
            x = xconv[0]
        except (TypeError, IndexError, KeyError):
            x = xconv
        delist = False
        if (not np.iterable(dx)):
            dx = [dx]
            delist = True
        dx = [(convert((x0 + ddx)) - x) for ddx in dx]
        if delist:
            dx = dx[0]
    except (TypeError, AttributeError) as e:
        dx = convert(dx)
    return dx
