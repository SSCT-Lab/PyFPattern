def cases_test_moments():
    fail_normalization = set(['vonmises', 'ksone'])
    fail_higher = set(['vonmises', 'ksone', 'ncf'])
    for (distname, arg) in (distcont[:] + [(histogram_test_instance, tuple())]):
        if (distname == 'levy_stable'):
            continue
        cond1 = (distname not in fail_normalization)
        cond2 = (distname not in fail_higher)
        (yield (distname, arg, cond1, cond2))
        if ((not cond1) or (not cond2)):
            (yield pytest.param(distname, arg, True, True, marks=pytest.mark.xfail))