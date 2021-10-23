def _solve_cg(lap_sparse, B, tol, return_full_prob=False):
    '\n    solves lap_sparse X_i = B_i for each phase i, using the conjugate\n    gradient method. For each pixel, the label i corresponding to the\n    maximal X_i is returned.\n    '
    lap_sparse = lap_sparse.tocsc()
    X = []
    for i in range(len(B)):
        x0 = cg(lap_sparse, (- B[i].todense()), tol=tol)[0]
        X.append(x0)
    if (not return_full_prob):
        X = np.array(X)
        X = np.argmax(X, axis=0)
    return X