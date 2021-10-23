def _wavelet_threshold(img, wavelet, threshold=None, sigma=None, mode='soft', wavelet_levels=None):
    'Perform wavelet thresholding.\n\n    Parameters\n    ----------\n    img : ndarray (2d or 3d) of ints, uints or floats\n        Input data to be denoised. `img` can be of any numeric type,\n        but it is cast into an ndarray of floats for the computation\n        of the denoised image.\n    wavelet : string\n        The type of wavelet to perform. Can be any of the options\n        pywt.wavelist outputs. For example, this may be any of ``{db1, db2,\n        db3, db4, haar}``.\n    sigma : float, optional\n        The standard deviation of the noise. The noise is estimated when sigma\n        is None (the default) by the method in [2]_.\n    threshold : float, optional\n        The thresholding value. All wavelet coefficients less than this value\n        are set to 0. The default value (None) uses the BayesShrink method\n        found in [1]_ to remove noise.\n    mode : {\'soft\', \'hard\'}, optional\n        An optional argument to choose the type of denoising performed. It\n        noted that choosing soft thresholding given additive noise finds the\n        best approximation of the original image.\n    wavelet_levels : int or None, optional\n        The number of wavelet decomposition levels to use.  The default is\n        three less than the maximum number of possible decomposition levels\n        (see Notes below).\n\n    Returns\n    -------\n    out : ndarray\n        Denoised image.\n\n    References\n    ----------\n    .. [1] Chang, S. Grace, Bin Yu, and Martin Vetterli. "Adaptive wavelet\n           thresholding for image denoising and compression." Image Processing,\n           IEEE Transactions on 9.9 (2000): 1532-1546.\n           DOI: 10.1109/83.862633\n    .. [2] D. L. Donoho and I. M. Johnstone. "Ideal spatial adaptation\n           by wavelet shrinkage." Biometrika 81.3 (1994): 425-455.\n           DOI: 10.1093/biomet/81.3.425\n\n    '
    wavelet = pywt.Wavelet(wavelet)
    if (wavelet_levels is None):
        dlen = wavelet.dec_len
        wavelet_levels = np.min([pywt.dwt_max_level(s, dlen) for s in img.shape])
        wavelet_levels = max((wavelet_levels - 3), 1)
    coeffs = pywt.wavedecn(img, wavelet=wavelet, level=wavelet_levels)
    dcoeffs = coeffs[1:]
    if (sigma is None):
        detail_coeffs = dcoeffs[(- 1)][('d' * img.ndim)]
        sigma = _sigma_est_dwt(detail_coeffs, distribution='Gaussian')
    if (threshold is None):
        var = (sigma ** 2)
        threshold = [{key: _bayes_thresh(level[key], var) for key in level} for level in dcoeffs]
    if np.isscalar(threshold):
        denoised_detail = [{key: pywt.threshold(level[key], value=threshold, mode=mode) for key in level} for level in dcoeffs]
    else:
        denoised_detail = [{key: pywt.threshold(level[key], value=thresh[key], mode=mode) for key in level} for (thresh, level) in zip(threshold, dcoeffs)]
    denoised_coeffs = ([coeffs[0]] + denoised_detail)
    return pywt.waverecn(denoised_coeffs, wavelet)