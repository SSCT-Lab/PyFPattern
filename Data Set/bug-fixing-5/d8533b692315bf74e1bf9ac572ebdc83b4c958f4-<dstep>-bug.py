def dstep(system, x0=None, t=None, n=None):
    '\n    Step response of discrete-time system.\n\n    Parameters\n    ----------\n    system : tuple of array_like\n        A tuple describing the system.\n        The following gives the number of elements in the tuple and\n        the interpretation:\n\n            * 1: (instance of `dlti`)\n            * 3: (num, den, dt)\n            * 4: (zeros, poles, gain, dt)\n            * 5: (A, B, C, D, dt)\n\n    x0 : array_like, optional\n        Initial state-vector.  Defaults to zero.\n    t : array_like, optional\n        Time points.  Computed if not given.\n    n : int, optional\n        The number of time points to compute (if `t` is not given).\n\n    Returns\n    -------\n    tout : ndarray\n        Output time points, as a 1-D array.\n    yout : ndarray\n        Step response of system.  Each element of the tuple represents\n        the output of the system based on a step response to each input.\n\n    See Also\n    --------\n    step, dimpulse, dlsim, cont2discrete\n\n    '
    if isinstance(system, dlti):
        system = system._as_ss()
    elif isinstance(system, lti):
        raise AttributeError('dstep can only be used with discrete-time dlti systems.')
    else:
        system = dlti(*system[:(- 1)], dt=system[(- 1)])._as_ss()
    if (n is None):
        n = 100
    if (t is None):
        t = np.linspace(0, (n * system.dt), n, endpoint=False)
    else:
        t = np.asarray(t)
    yout = None
    for i in range(0, system.inputs):
        u = np.zeros((t.shape[0], system.inputs))
        u[:, i] = np.ones((t.shape[0],))
        one_output = dlsim(system, u, t=t, x0=x0)
        if (yout is None):
            yout = (one_output[1],)
        else:
            yout = (yout + (one_output[1],))
        tout = one_output[0]
    return (tout, yout)