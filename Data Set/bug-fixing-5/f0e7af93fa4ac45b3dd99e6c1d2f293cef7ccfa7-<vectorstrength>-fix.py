def vectorstrength(events, period):
    '\n    Determine the vector strength of the events corresponding to the given\n    period.\n\n    The vector strength is a measure of phase synchrony, how well the\n    timing of the events is synchronized to a single period of a periodic\n    signal.\n\n    If multiple periods are used, calculate the vector strength of each.\n    This is called the "resonating vector strength".\n\n    Parameters\n    ----------\n    events : 1D array_like\n        An array of time points containing the timing of the events.\n    period : float or array_like\n        The period of the signal that the events should synchronize to.\n        The period is in the same units as `events`.  It can also be an array\n        of periods, in which case the outputs are arrays of the same length.\n\n    Returns\n    -------\n    strength : float or 1D array\n        The strength of the synchronization.  1.0 is perfect synchronization\n        and 0.0 is no synchronization.  If `period` is an array, this is also\n        an array with each element containing the vector strength at the\n        corresponding period.\n    phase : float or array\n        The phase that the events are most strongly synchronized to in radians.\n        If `period` is an array, this is also an array with each element\n        containing the phase for the corresponding period.\n\n    References\n    ----------\n    van Hemmen, JL, Longtin, A, and Vollmayr, AN. Testing resonating vector\n        strength: Auditory system, electric fish, and noise.\n        Chaos 21, 047508 (2011);\n        :doi:`10.1063/1.3670512`.\n    van Hemmen, JL.  Vector strength after Goldberg, Brown, and von Mises:\n        biological and mathematical perspectives.  Biol Cybern.\n        2013 Aug;107(4):385-96. :doi:`10.1007/s00422-013-0561-7`.\n    van Hemmen, JL and Vollmayr, AN.  Resonating vector strength: what happens\n        when we vary the "probing" frequency while keeping the spike times\n        fixed.  Biol Cybern. 2013 Aug;107(4):491-94.\n        :doi:`10.1007/s00422-013-0560-8`.\n    '
    events = np.asarray(events)
    period = np.asarray(period)
    if (events.ndim > 1):
        raise ValueError('events cannot have dimensions more than 1')
    if (period.ndim > 1):
        raise ValueError('period cannot have dimensions more than 1')
    scalarperiod = (not period.ndim)
    events = np.atleast_2d(events)
    period = np.atleast_2d(period)
    if (period <= 0).any():
        raise ValueError('periods must be positive')
    vectors = np.exp(np.dot(((2j * np.pi) / period.T), events))
    vectormean = np.mean(vectors, axis=1)
    strength = abs(vectormean)
    phase = np.angle(vectormean)
    if scalarperiod:
        strength = strength[0]
        phase = phase[0]
    return (strength, phase)