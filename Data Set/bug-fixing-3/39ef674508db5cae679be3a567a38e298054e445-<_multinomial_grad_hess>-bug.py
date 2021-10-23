def _multinomial_grad_hess(w, X, Y, alpha, sample_weight):
    '\n    Computes the gradient and the Hessian, in the case of a multinomial loss.\n\n    Parameters\n    ----------\n    w : ndarray, shape (n_classes * n_features,) or\n        (n_classes * (n_features + 1),)\n        Coefficient vector.\n\n    X : {array-like, sparse matrix}, shape (n_samples, n_features)\n        Training data.\n\n    Y : ndarray, shape (n_samples, n_classes)\n        Transformed labels according to the output of LabelBinarizer.\n\n    alpha : float\n        Regularization parameter. alpha is equal to 1 / C.\n\n    sample_weight : array-like, shape (n_samples,) optional\n        Array of weights that are assigned to individual samples.\n\n    Returns\n    -------\n    grad : array, shape (n_classes * n_features,) or\n        (n_classes * (n_features + 1),)\n        Ravelled gradient of the multinomial loss.\n\n    hessp : callable\n        Function that takes in a vector input of shape (n_classes * n_features)\n        or (n_classes * (n_features + 1)) and returns matrix-vector product\n        with hessian.\n\n    References\n    ----------\n    Barak A. Pearlmutter (1993). Fast Exact Multiplication by the Hessian.\n        http://www.bcl.hamilton.ie/~barak/papers/nc-hessian.pdf\n    '
    n_features = X.shape[1]
    n_classes = Y.shape[1]
    fit_intercept = (w.size == (n_classes * (n_features + 1)))
    (loss, grad, p) = _multinomial_loss_grad(w, X, Y, alpha, sample_weight)
    sample_weight = sample_weight[:, np.newaxis]

    def hessp(v):
        v = v.reshape(n_classes, (- 1))
        if fit_intercept:
            inter_terms = v[:, (- 1)]
            v = v[:, :(- 1)]
        else:
            inter_terms = 0
        r_yhat = safe_sparse_dot(X, v.T)
        r_yhat += inter_terms
        r_yhat += ((- p) * r_yhat).sum(axis=1)[:, np.newaxis]
        r_yhat *= p
        r_yhat *= sample_weight
        hessProd = np.zeros((n_classes, (n_features + bool(fit_intercept))))
        hessProd[:, :n_features] = safe_sparse_dot(r_yhat.T, X)
        hessProd[:, :n_features] += (v * alpha)
        if fit_intercept:
            hessProd[:, (- 1)] = r_yhat.sum(axis=0)
        return hessProd.ravel()
    return (grad, hessp)