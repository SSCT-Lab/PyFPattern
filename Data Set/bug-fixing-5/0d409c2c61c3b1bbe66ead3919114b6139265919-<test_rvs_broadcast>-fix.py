def test_rvs_broadcast():
    skp = npt.dec.skipif
    for (dist, shape_args) in distcont:
        shape_only = (dist in ['betaprime', 'dgamma', 'exponnorm', 'nct', 'dweibull', 'rice', 'levy_stable', 'skewnorm'])
        distfunc = getattr(stats, dist)
        loc = np.zeros(2)
        scale = np.ones((3, 1))
        nargs = distfunc.numargs
        allargs = []
        bshape = [3, 2]
        for k in range(nargs):
            shp = (((k + 4),) + ((1,) * (k + 2)))
            allargs.append((shape_args[k] * np.ones(shp)))
            bshape.insert(0, (k + 4))
        allargs.extend([loc, scale])
        is_too_slow = (dist in ['gausshyper', 'genexpon'])
        check_rvs = skp(is_too_slow)(check_rvs_broadcast)
        (yield (check_rvs, distfunc, dist, allargs, bshape, shape_only, 'd'))