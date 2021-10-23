def evalf_trig(v, prec, options):
    '\n    This function handles sin and cos of complex arguments.\n\n    TODO: should also handle tan of complex arguments.\n    '
    from sympy import cos, sin
    if (v.func is cos):
        func = mpf_cos
    elif (v.func is sin):
        func = mpf_sin
    else:
        raise NotImplementedError
    arg = v.args[0]
    xprec = (prec + 20)
    (re, im, re_acc, im_acc) = evalf(arg, xprec, options)
    if im:
        if ('subs' in options):
            v = v.subs(options['subs'])
        return evalf(v._eval_evalf(prec), prec, options)
    if (not re):
        if (v.func is cos):
            return (fone, None, prec, None)
        elif (v.func is sin):
            return (None, None, None, None)
        else:
            raise NotImplementedError
    xsize = fastlog(re)
    if (xsize < 1):
        return (func(re, prec, rnd), None, prec, None)
    if (xsize >= 10):
        xprec = (prec + xsize)
        (re, im, re_acc, im_acc) = evalf(arg, xprec, options)
    while 1:
        y = func(re, prec, rnd)
        ysize = fastlog(y)
        gap = (- ysize)
        accuracy = ((xprec - xsize) - gap)
        if (accuracy < prec):
            if options.get('verbose'):
                print('SIN/COS', accuracy, 'wanted', prec, 'gap', gap)
                print(to_str(y, 10))
            if (xprec > options.get('maxprec', DEFAULT_MAXPREC)):
                return (y, None, accuracy, None)
            xprec += gap
            (re, im, re_acc, im_acc) = evalf(arg, xprec, options)
            continue
        else:
            return (y, None, prec, None)