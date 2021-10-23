def _product(*iters):
    '\n    cartesian product generator\n\n    Notes\n    =====\n\n    Unlike itertools.product, it works also with iterables which do not fit\n    in memory. See http://bugs.python.org/issue10109\n\n    Author: Fernando Sumudu\n    with small changes\n    '
    import itertools
    inf_iters = tuple((itertools.cycle(enumerate(it)) for it in iters))
    num_iters = len(inf_iters)
    cur_val = ([None] * num_iters)
    first_v = True
    while True:
        (i, p) = (0, num_iters)
        while (p and (not i)):
            p -= 1
            (i, cur_val[p]) = next(inf_iters[p])
        if ((not p) and (not i)):
            if first_v:
                first_v = False
            else:
                break
        (yield cur_val)