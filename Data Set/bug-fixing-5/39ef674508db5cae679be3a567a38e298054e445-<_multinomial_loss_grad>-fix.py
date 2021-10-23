def _multinomial_loss_grad(w, X, Y, alpha, sample_weight):
    'Computes the multinomial loss, gradient and class probabilities.\n\n    Parameters\n    ----------\n    w : ndarray, shape (n_classes * n_features,) or\n        (n_classes * (n_features + 1),)\n        Coefficient vector.\n\n    X : {array-like, sparse matrix}, shape (n_samples, n_features)\n        Training data.\n\n    Y : ndarray, shape (n_samples, n_classes)\n        Transformed labels according to the output of LabelBinarizer.\n\n    alpha : float\n        Regularization parameter. alpha is equal to 1 / C.\n\n    sample_weight : array-like, shape (n_samples,)\n        Array of weights that are assigned to individual samples.\n\n    Returns\n    -------\n    loss : float\n        Multinomial loss.\n\n    grad : ndarray, shape (n_classes * n_features,) or\n        (n_classes * (n_features + 1),)\n        Ravelled gradient of the multinomial loss.\n\n    p : ndarray, shape (n_samples, n_classes)\n        Estimated class probabilities\n\n    Reference\n    ---------\n    Bishop, C. M. (2006). Pattern recognition and machine learning.\n    Springer. (Chapter 4.3.4)\n    '
    n_classes = Y.shape[1]
    n_features = X.shape[1]
    fit_intercept = (w.size == (n_classes * (n_features + 1)))
    grad = np.zeros((n_classes, (n_features + bool(fit_intercept))), dtype=X.dtype)
    (loss, p, w) = _multinomial_loss(w, X, Y, alpha, sample_weight)
    sample_weight = sample_weight[:, np.newaxis]
    diff = (sample_weight * (p - Y))
    grad[:, :n_features] = safe_sparse_dot(diff.T, X)
    grad[:, :n_features] += (alpha * w)
    if fit_intercept:
        grad[:, (- 1)] = diff.sum(axis=0)
    return (loss, grad.ravel(), p)