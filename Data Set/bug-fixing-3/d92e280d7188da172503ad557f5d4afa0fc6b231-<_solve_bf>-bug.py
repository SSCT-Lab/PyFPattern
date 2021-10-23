def _solve_bf(lap_sparse, B, return_full_prob=False):
    '\n    solves lap_sparse X_i = B_i for each phase i. An LU decomposition\n    of lap_sparse is computed first. For each pixel, the label i\n    corresponding to the maximal X_i is returned.\n    '
    lap_sparse = lap_sparse.tocsc()
    solver = sparse.linalg.factorized(lap_sparse.astype(np.double))
    X = np.array([solver(np.array((- B[i]).todense()).ravel()) for i in range(len(B))])
    if (not return_full_prob):
        X = np.argmax(X, axis=0)
    return X