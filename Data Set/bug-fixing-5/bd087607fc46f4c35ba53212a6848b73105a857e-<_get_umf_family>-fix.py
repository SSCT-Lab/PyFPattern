def _get_umf_family(A):
    'Get umfpack family string given the sparse matrix dtype.'
    _families = {
        (np.float64, np.int32): 'di',
        (np.complex128, np.int32): 'zi',
        (np.float64, np.int64): 'dl',
        (np.complex128, np.int64): 'zl',
    }
    f_type = np.sctypeDict[A.dtype.name]
    i_type = np.sctypeDict[A.indices.dtype.name]
    try:
        family = _families[(f_type, i_type)]
    except KeyError:
        msg = ('only float64 or complex128 matrices with int32 or int64 indices are supported! (got: matrix: %s, indices: %s)' % (f_type, i_type))
        raise ValueError(msg)
    return family