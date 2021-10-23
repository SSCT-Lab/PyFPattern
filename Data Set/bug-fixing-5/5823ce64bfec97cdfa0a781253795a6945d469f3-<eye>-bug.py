@set_module('mxnet.symbol.numpy')
def eye(N, M=None, k=0, dtype=_np.float32, **kwargs):
    '\n    Return a 2-D array with ones on the diagonal and zeros elsewhere.\n\n    Parameters\n    ----------\n    N : int\n        Number of rows in the output.\n    M : int, optional\n        Number of columns in the output. If None, defaults to N.\n    k : int, optional\n        Index of the diagonal: 0 (the default) refers to the main diagonal,\n        a positive value refers to an upper diagonal,\n        and a negative value to a lower diagonal.\n    dtype : data-type, optional\n        Data-type of the returned array.\n\n    Returns\n    -------\n    I : ndarray of shape (N,M)\n        An array where all elements are equal to zero,\n        except for the k-th diagonal, whose values are equal to one.\n    '
    _sanity_check_params('eye', ['order'], kwargs)
    ctx = kwargs.pop('ctx', current_context())
    if (ctx is None):
        ctx = current_context()
    return _npi.eye(N, M, k, ctx, dtype)