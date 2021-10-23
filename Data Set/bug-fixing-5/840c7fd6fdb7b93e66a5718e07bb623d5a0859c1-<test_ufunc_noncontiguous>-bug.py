@pytest.mark.parametrize('ufunc', [getattr(np, x) for x in dir(np) if isinstance(getattr(np, x), np.ufunc)])
def test_ufunc_noncontiguous(ufunc):
    '\n    Check that contiguous and non-contiguous calls to ufuncs\n    have the same results for values in range(9)\n    '
    for typ in ufunc.types:
        if any((set('O?mM') & set(typ))):
            continue
        (inp, out) = typ.split('->')
        args_c = [np.empty(6, t) for t in inp]
        args_n = [np.empty(18, t)[::3] for t in inp]
        for a in args_c:
            a.flat = range(1, 7)
        for a in args_n:
            a.flat = range(1, 7)
        with warnings.catch_warnings(record=True):
            warnings.filterwarnings('always')
            res_c = ufunc(*args_c)
            res_n = ufunc(*args_n)
        assert_equal(res_c, res_n)