def compare_ssim(X, Y, win_size=None, gradient=False, data_range=None, multichannel=False, gaussian_weights=False, full=False, **kwargs):
    'Compute the mean structural similarity index between two images.\n\n    Parameters\n    ----------\n    X, Y : ndarray\n        Image. Any dimensionality.\n    win_size : int or None\n        The side-length of the sliding window used in comparison. Must be an\n        odd value. If `gaussian_weights` is True, this is ignored and the\n        window size will depend on `sigma`.\n    gradient : bool, optional\n        If True, also return the gradient with respect to Y.\n    data_range : float, optional\n        The data range of the input image (distance between minimum and\n        maximum possible values). By default, this is estimated from the image\n        data-type.\n    multichannel : bool, optional\n        If True, treat the last dimension of the array as channels. Similarity\n        calculations are done independently for each channel then averaged.\n    gaussian_weights : bool, optional\n        If True, each patch has its mean and variance spatially weighted by a\n        normalized Gaussian kernel of width sigma=1.5.\n    full : bool, optional\n        If True, return the full structural similarity image instead of the\n        mean value.\n\n    Other Parameters\n    ----------------\n    use_sample_covariance : bool\n        If True, normalize covariances by N-1 rather than, N where N is the\n        number of pixels within the sliding window.\n    K1 : float\n        Algorithm parameter, K1 (small constant, see [1]_).\n    K2 : float\n        Algorithm parameter, K2 (small constant, see [1]_).\n    sigma : float\n        Standard deviation for the Gaussian when `gaussian_weights` is True.\n\n    Returns\n    -------\n    mssim : float\n        The mean structural similarity over the image.\n    grad : ndarray\n        The gradient of the structural similarity index between X and Y [2]_.\n        This is only returned if `gradient` is set to True.\n    S : ndarray\n        The full SSIM image.  This is only returned if `full` is set to True.\n\n    Notes\n    -----\n    To match the implementation of Wang et. al. [1]_, set `gaussian_weights`\n    to True, `sigma` to 1.5, and `use_sample_covariance` to False.\n\n    References\n    ----------\n    .. [1] Wang, Z., Bovik, A. C., Sheikh, H. R., & Simoncelli, E. P.\n       (2004). Image quality assessment: From error visibility to\n       structural similarity. IEEE Transactions on Image Processing,\n       13, 600-612.\n       https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf,\n       :DOI:`10.1109/TIP.2003.819861`\n\n    .. [2] Avanaki, A. N. (2009). Exact global histogram specification\n       optimized for structural similarity. Optical Review, 16, 613-621.\n       :arXiv:`0901.0065`\n       :DOI:`10.1007/s10043-009-0119-z`\n\n    '
    if (not (X.shape == Y.shape)):
        raise ValueError('Input images must have the same dimensions.')
    if multichannel:
        args = dict(win_size=win_size, gradient=gradient, data_range=data_range, multichannel=False, gaussian_weights=gaussian_weights, full=full)
        args.update(kwargs)
        nch = X.shape[(- 1)]
        mssim = np.empty(nch)
        if gradient:
            G = np.empty(X.shape)
        if full:
            S = np.empty(X.shape)
        for ch in range(nch):
            ch_result = compare_ssim(X[(..., ch)], Y[(..., ch)], **args)
            if (gradient and full):
                (mssim[(..., ch)], G[(..., ch)], S[(..., ch)]) = ch_result
            elif gradient:
                (mssim[(..., ch)], G[(..., ch)]) = ch_result
            elif full:
                (mssim[(..., ch)], S[(..., ch)]) = ch_result
            else:
                mssim[(..., ch)] = ch_result
        mssim = mssim.mean()
        if (gradient and full):
            return (mssim, G, S)
        elif gradient:
            return (mssim, G)
        elif full:
            return (mssim, S)
        else:
            return mssim
    K1 = kwargs.pop('K1', 0.01)
    K2 = kwargs.pop('K2', 0.03)
    sigma = kwargs.pop('sigma', 1.5)
    if (K1 < 0):
        raise ValueError('K1 must be positive')
    if (K2 < 0):
        raise ValueError('K2 must be positive')
    if (sigma < 0):
        raise ValueError('sigma must be positive')
    use_sample_covariance = kwargs.pop('use_sample_covariance', True)
    if gaussian_weights:
        truncate = 3.5
    if (win_size is None):
        if gaussian_weights:
            r = int(((truncate * sigma) + 0.5))
            win_size = ((2 * r) + 1)
        else:
            win_size = 7
    if np.any(((np.asarray(X.shape) - win_size) < 0)):
        raise ValueError('win_size exceeds image extent.  If the input is a multichannel (color) image, set multichannel=True.')
    if (not ((win_size % 2) == 1)):
        raise ValueError('Window size must be odd.')
    if (data_range is None):
        if (X.dtype != Y.dtype):
            warn('Inputs have mismatched dtype.  Setting data_range based on X.dtype.')
        (dmin, dmax) = dtype_range[X.dtype.type]
        data_range = (dmax - dmin)
    ndim = X.ndim
    if gaussian_weights:
        filter_func = gaussian_filter
        filter_args = {
            'sigma': sigma,
            'truncate': truncate,
        }
    else:
        filter_func = uniform_filter
        filter_args = {
            'size': win_size,
        }
    X = X.astype(np.float64)
    Y = Y.astype(np.float64)
    NP = (win_size ** ndim)
    if use_sample_covariance:
        cov_norm = (NP / (NP - 1))
    else:
        cov_norm = 1.0
    ux = filter_func(X, **filter_args)
    uy = filter_func(Y, **filter_args)
    uxx = filter_func((X * X), **filter_args)
    uyy = filter_func((Y * Y), **filter_args)
    uxy = filter_func((X * Y), **filter_args)
    vx = (cov_norm * (uxx - (ux * ux)))
    vy = (cov_norm * (uyy - (uy * uy)))
    vxy = (cov_norm * (uxy - (ux * uy)))
    R = data_range
    C1 = ((K1 * R) ** 2)
    C2 = ((K2 * R) ** 2)
    (A1, A2, B1, B2) = ((((2 * ux) * uy) + C1), ((2 * vxy) + C2), (((ux ** 2) + (uy ** 2)) + C1), ((vx + vy) + C2))
    D = (B1 * B2)
    S = ((A1 * A2) / D)
    pad = ((win_size - 1) // 2)
    mssim = crop(S, pad).mean()
    if gradient:
        grad = (filter_func((A1 / D), **filter_args) * X)
        grad += (filter_func(((- S) / B2), **filter_args) * Y)
        grad += filter_func((((ux * (A2 - A1)) - ((uy * (B2 - B1)) * S)) / D), **filter_args)
        grad *= (2 / X.size)
        if full:
            return (mssim, grad, S)
        else:
            return (mssim, grad)
    elif full:
        return (mssim, S)
    else:
        return mssim