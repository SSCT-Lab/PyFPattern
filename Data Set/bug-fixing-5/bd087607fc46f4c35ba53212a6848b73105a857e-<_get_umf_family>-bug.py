def _get_umf_family(A):
    'Get umfpack family string given the sparse matrix dtype.'
    family = {
        'di': 'di',
        'Di': 'zi',
        'dl': 'dl',
        'Dl': 'zl',
    }
    dt = (A.dtype.char + A.indices.dtype.char)
    return family[dt]