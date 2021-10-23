def _chirp_phase(t, f0, t1, f1, method='linear', vertex_zero=True):
    '\n    Calculate the phase used by `chirp` to generate its output.\n\n    See `chirp` for a description of the arguments.\n\n    '
    t = asarray(t)
    f0 = float(f0)
    t1 = float(t1)
    f1 = float(f1)
    if (method in ['linear', 'lin', 'li']):
        beta = ((f1 - f0) / t1)
        phase = ((2 * pi) * ((f0 * t) + (((0.5 * beta) * t) * t)))
    elif (method in ['quadratic', 'quad', 'q']):
        beta = ((f1 - f0) / (t1 ** 2))
        if vertex_zero:
            phase = ((2 * pi) * ((f0 * t) + ((beta * (t ** 3)) / 3)))
        else:
            phase = ((2 * pi) * ((f1 * t) + ((beta * (((t1 - t) ** 3) - (t1 ** 3))) / 3)))
    elif (method in ['logarithmic', 'log', 'lo']):
        if ((f0 * f1) <= 0.0):
            raise ValueError('For a logarithmic chirp, f0 and f1 must be nonzero and have the same sign.')
        if (f0 == f1):
            phase = (((2 * pi) * f0) * t)
        else:
            beta = (t1 / log((f1 / f0)))
            phase = ((((2 * pi) * beta) * f0) * (pow((f1 / f0), (t / t1)) - 1.0))
    elif (method in ['hyperbolic', 'hyp']):
        if ((f0 == 0) or (f1 == 0)):
            raise ValueError('For a hyperbolic chirp, f0 and f1 must be nonzero.')
        if (f0 == f1):
            phase = (((2 * pi) * f0) * t)
        else:
            sing = (((- f1) * t1) / (f0 - f1))
            phase = (((2 * pi) * ((- sing) * f0)) * log(np.abs((1 - (t / sing)))))
    else:
        raise ValueError(("method must be 'linear', 'quadratic', 'logarithmic', or 'hyperbolic', but a value of %r was given." % method))
    return phase