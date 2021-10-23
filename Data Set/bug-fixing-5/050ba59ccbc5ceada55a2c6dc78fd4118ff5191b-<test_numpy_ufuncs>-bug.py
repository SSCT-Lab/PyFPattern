@pytest.mark.parametrize('func', [np.exp, np.exp2, np.expm1, np.log, np.log2, np.log10, np.log1p, np.sqrt, np.sin, np.cos, np.tan, np.arcsin, np.arccos, np.arctan, np.sinh, np.cosh, np.tanh, np.arcsinh, np.arccosh, np.arctanh, np.deg2rad, np.rad2deg], ids=(lambda func: func.__name__))
def test_numpy_ufuncs(idx, func):
    if _np_version_under1p17:
        expected_exception = AttributeError
        msg = "'tuple' object has no attribute '{}'".format(func.__name__)
    else:
        expected_exception = TypeError
        msg = 'loop of ufunc does not support argument 0 of type tuple which has no callable {} method'.format(func.__name__)
    with pytest.raises(expected_exception, match=msg):
        func(idx)