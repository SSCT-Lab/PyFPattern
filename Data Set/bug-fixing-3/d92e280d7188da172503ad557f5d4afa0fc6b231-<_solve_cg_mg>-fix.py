def _solve_cg_mg(lap_sparse, B, tol, return_full_prob=False):
    '\n    solves lap_sparse X_i = B_i for each phase i, using the conjugate\n    gradient method with a multigrid preconditioner (ruge-stuben from\n    pyamg). For each pixel, the label i corresponding to the maximal\n    X_i is returned.\n    '
    X = []
    ml = ruge_stuben_solver(lap_sparse)
    M = ml.aspreconditioner(cycle='V')
    for i in range(len(B)):
        x0 = cg(lap_sparse, (- B[i].toarray()), tol=tol, M=M, maxiter=30)[0]
        X.append(x0)
    if (not return_full_prob):
        X = np.array(X)
        X = np.argmax(X, axis=0)
    return X