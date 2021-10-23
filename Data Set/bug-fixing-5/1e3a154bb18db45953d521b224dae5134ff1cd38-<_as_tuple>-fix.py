def _as_tuple(xs):
    if isinstance(xs, tuple):
        return xs
    elif isinstance(xs, list):
        return tuple(xs)
    else:
        return (xs,)