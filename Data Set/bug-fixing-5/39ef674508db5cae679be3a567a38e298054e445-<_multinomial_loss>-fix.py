def _multinomial_loss(w, X, Y, alpha, sample_weight):
    'Computes multinomial loss and class probabilities.\n\n    Parameters\n    ----------\n    w : ndarray, shape (n_classes * n_features,) or\n        (n_classes * (n_features + 1),)\n        Coefficient vector.\n\n    X : {array-like, sparse matrix}, shape (n_samples, n_features)\n        Training data.\n\n    Y : ndarray, shape (n_samples, n_classes)\n        Transformed labels according to the output of LabelBinarizer.\n\n    alpha : float\n        Regularization parameter. alpha is equal to 1 / C.\n\n    sample_weight : array-like, shape (n_samples,)\n        Array of weights that are assigned to individual samples.\n\n    Returns\n    -------\n    loss : float\n        Multinomial loss.\n\n    p : ndarray, shape (n_samples, n_classes)\n        Estimated class probabilities.\n\n    w : ndarray, shape (n_classes, n_features)\n        Reshaped param vector excluding intercept terms.\n\n    Reference\n    ---------\n    Bishop, C. M. (2006). Pattern recognition and machine learning.\n    Springer. (Chapter 4.3.4)\n    '
    n_classes = Y.shape[1]
    n_features = X.shape[1]
    fit_intercept = (w.size == (n_classes * (n_features + 1)))
    w = w.reshape(n_classes, (- 1))
    sample_weight = sample_weight[:, np.newaxis]
    if fit_intercept:
        intercept = w[:, (- 1)]
        w = w[:, :(- 1)]
    else:
        intercept = 0
    p = safe_sparse_dot(X, w.T)
    p += intercept
    p -= logsumexp(p, axis=1)[:, np.newaxis]
    loss = (- ((sample_weight * Y) * p).sum())
    loss += ((0.5 * alpha) * squared_norm(w))
    p = np.exp(p, p)
    return (loss, p, w)