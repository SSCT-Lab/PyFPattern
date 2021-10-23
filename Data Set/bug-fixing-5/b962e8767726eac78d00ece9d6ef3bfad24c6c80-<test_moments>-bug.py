@pytest.mark.slow
@pytest.mark.parametrize('distname,arg,normalization_ok,higher_ok', cases_test_moments())
def test_moments(distname, arg, normalization_ok, higher_ok):
    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'rv_histogram_instance'
    with suppress_warnings() as sup:
        sup.filter(IntegrationWarning, 'The integral is probably divergent, or slowly convergent.')
        sup.filter(category=DeprecationWarning, message='.*frechet_')
        (m, v, s, k) = distfn.stats(*arg, moments='mvsk')
        if normalization_ok:
            check_normalization(distfn, arg, distname)
        if higher_ok:
            check_mean_expect(distfn, arg, m, distname)
            check_skew_expect(distfn, arg, m, v, s, distname)
            check_var_expect(distfn, arg, m, v, distname)
            check_kurt_expect(distfn, arg, m, v, k, distname)
        check_loc_scale(distfn, arg, m, v, distname)
        check_moment(distfn, arg, m, v, distname)