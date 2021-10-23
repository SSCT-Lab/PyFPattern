

def frangi(image, sigmas=range(1, 10, 2), scale_range=None, scale_step=None, beta1=None, beta2=None, alpha=0.5, beta=0.5, gamma=15, black_ridges=True):
    "\n    Filter an image with the Frangi vesselness filter.\n\n    This filter can be used to detect continuous ridges, e.g. vessels,\n    wrinkles, rivers. It can be used to calculate the fraction of the\n    whole image containing such objects.\n\n    Defined only for 2-D and 3-D images. Calculates the eigenvectors of the\n    Hessian to compute the similarity of an image region to vessels, according\n    to the method described in [1]_.\n\n    Parameters\n    ----------\n    image : (N, M[, P]) ndarray\n        Array with input image data.\n    sigmas : iterable of floats, optional\n        Sigmas used as scales of filter, i.e.,\n        np.arange(scale_range[0], scale_range[1], scale_step)\n    scale_range : 2-tuple of floats, optional\n        The range of sigmas used.\n    scale_step : float, optional\n        Step size between sigmas.\n    alpha : float, optional\n        Frangi correction constant that adjusts the filter's\n        sensitivity to deviation from a plate-like structure.\n    beta = beta1 : float, optional\n        Frangi correction constant that adjusts the filter's\n        sensitivity to deviation from a blob-like structure.\n    gamma = beta2 : float, optional\n        Frangi correction constant that adjusts the filter's\n        sensitivity to areas of high variance/texture/structure.\n    black_ridges : boolean, optional\n        When True (the default), the filter detects black ridges; when\n        False, it detects white ridges.\n\n    Returns\n    -------\n    out : (N, M[, P]) ndarray\n        Filtered image (maximum of pixels across all scales).\n\n    Notes\n    -----\n    Written by Marc Schrijver, November 2001\n    Re-Written by D. J. Kroon, University of Twente, May 2009, [2]_\n    Adoption of 3D version from D. G. Ellis, Januar 20017, [3]_\n\n    See also\n    --------\n    meijering\n    sato\n    hessian\n\n    References\n    ----------\n    .. [1] Frangi, A. F., Niessen, W. J., Vincken, K. L., & Viergever, M. A.\n        (1998,). Multiscale vessel enhancement filtering. In International\n        Conference on Medical Image Computing and Computer-Assisted\n        Intervention (pp. 130-137). Springer Berlin Heidelberg.\n        :DOI:`10.1007/BFb0056195`\n    .. [2] Kroon, D. J.: Hessian based Frangi vesselness filter.\n    .. [3] Ellis, D. G.: https://github.com/ellisdg/frangi3d/tree/master/frangi\n    "
    if beta1:
        warn('Use keyword parameter `beta` instead of `beta1` which will be removed in version 0.17.', stacklevel=2)
        beta = beta1
    if beta2:
        warn('Use keyword parameter `gamma` instead of `beta2` which will be removed in version 0.17.', stacklevel=2)
        gamma = beta2
    if (scale_range and scale_step):
        warn('Use keyword parameter `sigmas` instead of `scale_range` and `scale_range` which will be removed in version 0.17.', stacklevel=2)
        sigmas = np.arange(scale_range[0], scale_range[1], scale_step)
    check_nD(image, [2, 3])
    sigmas = np.asarray(sigmas)
    if np.any((sigmas < 0.0)):
        raise ValueError('Sigma values less than zero are not valid')
    alpha_sq = (2 * (alpha ** 2))
    beta_sq = (2 * (beta ** 2))
    gamma_sq = (2 * (gamma ** 2))
    ndim = image.ndim
    if black_ridges:
        image = invert(image)
    filtered_array = np.zeros((sigmas.shape + image.shape))
    lambdas_array = np.zeros((sigmas.shape + image.shape))
    for (i, sigma) in enumerate(sigmas):
        (lambda1, *lambdas) = compute_hessian_eigenvalues(image, sigma, sorting='abs')
        r_a = (np.inf if (ndim == 2) else (_divide_nonzero(*lambdas) ** 2))
        filtered_raw = (np.abs(np.multiply.reduce(lambdas)) ** (1 / len(lambdas)))
        r_b = (_divide_nonzero(lambda1, filtered_raw) ** 2)
        r_g = sum(([(lambda1 ** 2)] + [(lambdai ** 2) for lambdai in lambdas]))
        filtered_array[i] = (((1 - np.exp(((- r_a) / alpha_sq))) * np.exp(((- r_b) / beta_sq))) * (1 - np.exp(((- r_g) / gamma_sq))))
        lambdas_array[i] = np.max(lambdas, axis=0)
    filtered_array[(lambdas_array > 0)] = 0
    return np.max(filtered_array, axis=0)
