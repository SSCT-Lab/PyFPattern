def blas(name, ndarray):
    return scipy.linalg.get_blas_funcs((name,), (ndarray,))[0]